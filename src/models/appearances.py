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
        appearances.append(appearance)

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
    with session.begin_transaction() as tx:
        for appearance in fetch_appearances():
            tx.run(
                """
                MATCH (p:Player {player_id: $player_id} )
                MATCH (g:Game {game_id: $game_id} )
                MERGE (p)-[r:APPEARED_IN]->(g)
                ON CREATE SET r.appearance_id = $appearance_id, 
                r.player_club_id = $player_club_id,
                r.yellow_cards = $yellow_cards,
                r.red_cards = $red_cards,
                r.goals = $goals,
                r.assists = $assists,
                r.minutes_played = $minutes_played
                """,
                player_id=appearance.player_id,
                game_id=appearance.game_id,
                appearance_id=appearance.appearance_id,
                player_club_id=appearance.player_club_id,
                yellow_cards=appearance.yellow_cards,
                red_cards=appearance.red_cards,
                goals=appearance.goals,
                assists=appearance.assists,
                minutes_played=appearance.minutes_played,
            )

        tx.commit()
