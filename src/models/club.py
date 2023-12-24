import logging
from typing import Optional

import neo4j
import numpy as np
from pydantic import BaseModel
from ..constants import *
import pandas as pd

logger = logging.getLogger(__name__)


class Club(BaseModel):
    club_id: int
    club_code: str
    name: str
    domestic_competition_id: str
    squad_size: int
    average_age: Optional[float] = None
    foreigners_number: int
    foreigners_percentage: Optional[float] = None
    national_team_players: int
    stadium_name: str
    stadium_seats: int
    net_transfer_record: str
    last_season: int
    url: str


def fetch_clubs():
    """
    Fetches clubs from SOURCE_PATH and returns a list of Club objects.
    """
    df = pd.read_csv(SOURCE_FOLDER + "/clubs.csv", sep=",")
    df = df.replace({np.nan: None})
    clubs = []
    for index, row in df.iterrows():
        club = Club(
            club_id=row["club_id"],
            club_code=row["club_code"],
            name=row["name"],
            domestic_competition_id=row["domestic_competition_id"],
            squad_size=row["squad_size"],
            average_age=row["average_age"],
            foreigners_number=row["foreigners_number"],
            foreigners_percentage=row["foreigners_percentage"],
            national_team_players=row["national_team_players"],
            stadium_name=row["stadium_name"],
            stadium_seats=row["stadium_seats"],
            net_transfer_record=row["net_transfer_record"],
            last_season=row["last_season"],
            url=row["url"],
        )
        clubs.append(club)
    return clubs


def create_club_constraints(session: neo4j.Session):
    """
    Creates constraints for the club nodes.
    """
    logger.info("Creating constraints for club nodes")
    with session.begin_transaction() as tx:
        tx.run(
            "CREATE CONSTRAINT IF NOT EXISTS FOR (club:Club) REQUIRE club.club_id IS UNIQUE"
        )
        tx.run(
            "CREATE INDEX IF NOT EXISTS FOR (club:Club) ON (club.name)"
        )

        tx.commit()


def create_clubs(session: neo4j.Session):
    """
    Creates club nodes.
    """
    logger.info("Creating club nodes")
    create_club_constraints(session)
    with session.begin_transaction() as tx:
        for club in fetch_clubs():
            tx.run(
                """
                MERGE (club:Club {club_id: $club_id})
                SET club.name = $name,
                club.club_code = $club_code,
                club.domestic_competition_id = $domestic_competition_id,
                club.squad_size = $squad_size,
                club.average_age = $average_age,
                club.foreigners_number = $foreigners_number,
                club.foreigners_percentage = $foreigners_percentage,
                club.national_team_players = $national_team_players,
                club.stadium_name = $stadium_name,
                club.stadium_seats = $stadium_seats,
                club.net_transfer_record = $net_transfer_record,
                club.last_season = $last_season,
                club.url = $url
                """,
                club_id=club.club_id,
                name=club.name,
                club_code=club.club_code,
                domestic_competition_id=club.domestic_competition_id,
                squad_size=club.squad_size,
                average_age=club.average_age,
                foreigners_number=club.foreigners_number,
                foreigners_percentage=club.foreigners_percentage,
                national_team_players=club.national_team_players,
                stadium_name=club.stadium_name,
                stadium_seats=club.stadium_seats,
                net_transfer_record=club.net_transfer_record,
                last_season=club.last_season,
                url=club.url,
            )
            tx.run(
                """
                MATCH (club:Club {club_id: $club_id})
                MATCH (competition:Competition {competition_id: $competition_id})
                MERGE (club)-[r:HAS_DOMESTIC_COMPETITION]->(competition)
                """,
                club_id=club.club_id,
                competition_id=club.domestic_competition_id,
            )

        tx.commit()

    logger.info("Clubs are created")
