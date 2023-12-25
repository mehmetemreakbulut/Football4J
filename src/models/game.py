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
        games.append(game.model_dump())
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
    games = fetch_games()
    batch_size = 10000
    for i in range(0, len(games), batch_size):
        logger.info(f"Creating game nodes {i} to {i+batch_size}")
        batch = games[i : i + batch_size]
        query = (
            "UNWIND $games as game "
            "MERGE (g:Game {game_id: game.game_id}) "
            "ON CREATE SET g.competition_id = game.competition_id, "
            "g.season = game.season, "
            "g.round = game.round, "
            "g.date = game.date, "
            "g.home_club_id = game.home_club_id, "
            "g.away_club_id = game.away_club_id, "
            "g.home_club_goals = game.home_club_goals, "
            "g.away_club_goals = game.away_club_goals, "
            "g.home_club_position = game.home_club_position, "
            "g.away_club_position = game.away_club_position, "
            "g.home_club_manager_name = game.home_club_manager_name, "
            "g.away_club_manager_name = game.away_club_manager_name, "
            "g.stadium = game.stadium, "
            "g.attendance = game.attendance, "
            "g.referee = game.referee, "
            "g.url = game.url, "
            "g.home_club_formation = game.home_club_formation, "
            "g.away_club_formation = game.away_club_formation "
            "MERGE (h:Club {club_id: game.home_club_id}) "
            "MERGE (a:Club {club_id: game.away_club_id}) "
            "MERGE (c:Competition {competition_id: game.competition_id}) "
            "MERGE (g)-[:HOME_CLUB]->(h) "
            "MERGE (g)-[:AWAY_CLUB]->(a) "
            "MERGE (g)-[:COMPETITION]->(c) "
        )



        games_with_referee = [game for game in batch if game["referee"]]
        games_with_stadium = [game for game in batch if game["stadium"]]

        query2 = (
            "UNWIND $games_with_referee as game "
            "MATCH (g:Game {game_id: game.game_id}) "
            "MERGE (r:Referee {name: game.referee}) "
            "MERGE (g)-[:REFEREE]->(r) "
        )

        query3 = (
            "UNWIND $games_with_stadium as game "
            "MATCH (g:Game {game_id: game.game_id}) "
            "MERGE (s:Stadium {name: game.stadium}) "
            "MERGE (g)-[:STADIUM]->(s) "
        )

        session.run(query, games=batch)
        session.run(query2, games_with_referee=games_with_referee)
        session.run(query3, games_with_stadium=games_with_stadium)


