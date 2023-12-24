import logging
from typing import Optional

import neo4j
import numpy as np
from pydantic import BaseModel
from ..constants import *
import pandas as pd


logger = logging.getLogger(__name__)


class Game(BaseModel):
    game_id: int
    competition_id: str
    season: int
    round: str
    date: str
    home_club_id: int
    away_club_id: int
    home_club_goals: int
    away_club_goals: int
    home_club_position: Optional[int] = None
    away_club_position: Optional[int] = None
    home_club_manager_name: Optional[str] = None
    away_club_manager_name: Optional[str] = None
    stadium: Optional[str] = None
    attendance: Optional[int] = None
    referee: Optional[str] = None
    url: str
    home_club_formation: Optional[str] = None
    away_club_formation: Optional[str] = None


def fetch_games():
    """
    Fetches competitions from SOURCE_PATH and returns a list of Competition objects.
    """
    df = pd.read_csv(SOURCE_FOLDER + "/games.csv", sep=",")
    df = df.replace({np.nan: None})
    games = []
    for index, row in df.iterrows():
        game = Game(
            game_id=row["game_id"],
            competition_id=row["competition_id"],
            season=row["season"],
            round=row["round"],
            date=row["date"],
            home_club_id=row["home_club_id"],
            away_club_id=row["away_club_id"],
            home_club_goals=row["home_club_goals"],
            away_club_goals=row["away_club_goals"],
            home_club_position=row["home_club_position"],
            away_club_position=row["away_club_position"],
            home_club_manager_name=row["home_club_manager_name"],
            away_club_manager_name=row["away_club_manager_name"],
            stadium=row["stadium"],
            attendance=row["attendance"],
            referee=row["referee"],
            url=row["url"],
            home_club_formation=row["home_club_formation"],
            away_club_formation=row["away_club_formation"],
        )
        games.append(game)
    return games


def create_game_constraints(session: neo4j.Session):
    """
    Creates constraints for the game nodes.
    """
    with session.begin_transaction() as tx:
        tx.run(
            "CREATE CONSTRAINT IF NOT EXISTS FOR (g:Game) REQUIRE g.game_id IS UNIQUE"
        )


def create_games(session: neo4j.Session):
    """
    Creates game nodes.
    """
    create_game_constraints(session)
    with session.begin_transaction() as tx:
        for game in fetch_games():
            tx.run(
                "MERGE (g:Game {game_id: $game_id}) "
                "ON CREATE SET g.competition_id = $competition_id, "
                "g.season = $season, "
                "g.round = $round, "
                "g.date = $date, "
                "g.home_club_id = $home_club_id, "
                "g.away_club_id = $away_club_id, "
                "g.home_club_goals = $home_club_goals, "
                "g.away_club_goals = $away_club_goals, "
                "g.home_club_position = $home_club_position, "
                "g.away_club_position = $away_club_position, "
                "g.home_club_manager_name = $home_club_manager_name, "
                "g.away_club_manager_name = $away_club_manager_name, "
                "g.stadium = $stadium, "
                "g.attendance = $attendance, "
                "g.referee = $referee, "
                "g.url = $url, "
                "g.home_club_formation = $home_club_formation, "
                "g.away_club_formation = $away_club_formation "
                ,
                game_id=game.game_id,
                competition_id=game.competition_id,
                season=game.season,
                round=game.round,
                date=game.date,
                home_club_id=game.home_club_id,
                away_club_id=game.away_club_id,
                home_club_goals=game.home_club_goals,
                away_club_goals=game.away_club_goals,
                home_club_position=game.home_club_position,
                away_club_position=game.away_club_position,
                home_club_manager_name=game.home_club_manager_name,
                away_club_manager_name=game.away_club_manager_name,
                stadium=game.stadium,
                attendance=game.attendance,
                referee=game.referee,
                url=game.url,
                home_club_formation=game.home_club_formation,
                away_club_formation=game.away_club_formation,
            )

            tx.run(
                """
                MATCH (g:Game {game_id: $game_id})
                MATCH (c:Club {club_id: $club_id})
                MERGE (g)-[r:HOME_CLUB]->(c)
                """,
                game_id=game.game_id,
                club_id=game.home_club_id,
            )


            tx.run(
                """
                MATCH (g:Game {game_id: $game_id})
                MATCH (c:Club {club_id: $club_id})
                MERGE (g)-[r:AWAY_CLUB]->(c)
                """,
                game_id=game.game_id,
                club_id=game.away_club_id,
            )


            tx.run(
                """
                MATCH (g:Game {game_id: $game_id})
                MATCH (c:Competition {competition_id: $competition_id})
                MERGE (g)-[r:COMPETITION]->(c)
                """,
                game_id=game.game_id,
                competition_id=game.competition_id,
            )



        tx.commit()

        logger.info("Created game nodes")