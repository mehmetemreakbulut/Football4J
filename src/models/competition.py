import logging
from typing import Optional

import neo4j
import numpy as np
from pydantic import BaseModel
from ..constants import *
import pandas as pd

logger = logging.getLogger(__name__)


class Competition(BaseModel):
    competition_id: str
    competition_code: str
    name: str
    sub_type: str
    type: str
    country_id: int
    country_name: Optional[str] = None
    domestic_league_code: Optional[str] = None
    confederation: str
    url: str


def fetch_competitions():
    """
    Fetches competitions from SOURCE_PATH and returns a list of Competition objects.
    """
    df = pd.read_csv(SOURCE_FOLDER + "/competitions.csv", sep=",")
    df = df.replace({np.nan: None})
    competitions = []
    for index, row in df.iterrows():
        competition = Competition(
            competition_id=row["competition_id"],
            competition_code=row["competition_code"],
            name=row["name"],
            sub_type=row["sub_type"],
            type=row["type"],
            country_id=row["country_id"],
            country_name=row["country_name"],
            domestic_league_code=row["domestic_league_code"],
            confederation=row["confederation"],
            url=row["url"],
        )
        competitions.append(competition)
    return competitions


def create_competition_constraints(session: neo4j.Session):
    """
    Creates constraints for the competition nodes.
    """
    logger.info("Creating constraints for competition nodes")
    with session.begin_transaction() as tx:
        tx.run(
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Competition) REQUIRE c.competition_id IS UNIQUE"
        )

        tx.run(
            "CREATE INDEX IF NOT EXISTS FOR (c:Competition) ON (c.name)"
        )

        tx.commit()


def create_competitions(session: neo4j.Session):
    """
    Creates competition nodes.
    """
    logger.info("Creating competition nodes")
    create_competition_constraints(session)
    with session.begin_transaction() as tx:
        for competition in fetch_competitions():
            tx.run(
                "MERGE (c:Competition {competition_id: $competition_id}) "
                "SET c.competition_code = $competition_code "
                "SET c.name = $name "
                "SET c.sub_type = $sub_type "
                "SET c.type = $type "
                "SET c.country_id = $country_id "
                "SET c.country_name = $country_name "
                "SET c.domestic_league_code = $domestic_league_code "
                "SET c.confederation = $confederation "
                "SET c.url = $url ",
                competition_id=competition.competition_id,
                competition_code=competition.competition_code,
                name=competition.name,
                sub_type=competition.sub_type,
                type=competition.type,
                country_id=competition.country_id,
                country_name=competition.country_name,
                domestic_league_code=competition.domestic_league_code,
                confederation=competition.confederation,
                url=competition.url,
            )

            if competition.country_name:
                tx.run(
                    """
                    MATCH (c:Competition {competition_id: $competition_id})
                    MERGE (co:Country {name: $country_name})
                    MERGE (c)-[:IN_COUNTRY]->(co)
                    """,
                    competition_id=competition.competition_id,
                    country_name=competition.country_name,
                )
        tx.commit()

    logger.info("Created competition nodes")