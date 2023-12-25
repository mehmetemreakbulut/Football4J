import logging
from typing import Optional

import neo4j
import numpy as np
from pydantic import BaseModel
import pandas as pd

from src.constants import SOURCE_FOLDER

logger = logging.getLogger(__name__)


class Appearance(BaseModel):
    appearance_id: int
    game_id: int
    player_id: int
    player_club_id: int
    player_current_club_id: int
    date: str
    player_name: Optional[str] = None
    competition_id: str
    yellow_cards: int
    red_cards: int
    goals: int
    assists: int
    minutes_played: int


def fetch_appearances():
    """
    Fetches appearances from SOURCE_PATH and returns a list of Appearance objects.
    """
    df = pd.read_csv(SOURCE_FOLDER + "/appearances.csv", sep=",")
    df = df.replace({np.nan: None})
    appearances = []
    for index, row in df.iterrows():
        appearance = Appearance(
            appearance_id=row["appearance_id"],
            game_id=row["game_id"],
            player_id=row["player_id"],
            player_club_id=row["player_club_id"],
            player_current_club_id=row["player_current_club_id"],
            date=row["date"],
            player_name=row["player_name"],
            competition_id=row["competition_id"],
            yellow_cards=row["yellow_cards"],
            red_cards=row["red_cards"],
            goals=row["goals"],
            assists=row["assists"],
            minutes_played=row["minutes_played"],
        )
        appearances.append(appearance.model_dump())

    return appearances


def create_constraints(session: neo4j.Session):
    """
    Creates constraints for the appearance nodes.
    """
    logger.info("Creating constraints for appearance nodes")
    with session.begin_transaction() as tx:
        tx.run(
            "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Appearance) REQUIRE a.appearance_id IS UNIQUE"
        )


def create_appearances(session: neo4j.Session):
    """
    Creates relationships between appearances and games.
    """
    logger.info("Creating relationships between appearances and games")
    create_constraints(session)
    appearances = fetch_appearances()
    query = """
    UNWIND $appearances AS appearance
    MATCH (p:Player {player_id: appearance.player_id})
    MATCH (g:Game {game_id: appearance.game_id})
    MERGE (p) - [r: APPEARED_IN]->(g) 
    ON CREATE SET
    r.appearance_id = appearance.appearance_id,
    r.player_club_id = appearance.player_club_id,
    r.date = appearance.date,
    r.yellow_cards = appearance.yellow_cards,
    r.red_cards = appearance.red_cards,
    r.goals = appearance.goals,
    r.assists = appearance.assists,
    r.minutes_played = appearance.minutes_played
    ON MATCH SET
    r.player_club_id = appearance.player_club_id
    """
    #create batches of 1000 appearances
    batch_size = 1000
    batches = [appearances[i:i + batch_size] for i in range(0, len(appearances), batch_size)]
    for i in range(len(batches)):
        batch = batches[i]
        logger.info(f"Creating relationships between appearances and games: batch {i+1}")
        session.run(query, appearances=batch)


    logger.info("Created relationships between appearances and games")
