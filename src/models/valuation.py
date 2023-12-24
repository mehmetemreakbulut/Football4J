import logging

import neo4j
from pydantic import BaseModel
from ..constants import *
import pandas as pd

logger = logging.getLogger(__name__)

class Valuation(BaseModel):
    player_id: int
    date: str
    market_value_in_eur: int
    current_club_id: int


def fetch_valuations():
    """
    Fetches valuations from SOURCE_PATH and returns a list of Valuation objects.
    """
    df = pd.read_csv(SOURCE_FOLDER + "/player_valuations.csv", sep=",")
    valuations = []
    for index, row in df.iterrows():
        valuation = Valuation(
            player_id=row["player_id"],
            date=row["date"],
            market_value_in_eur=row["market_value_in_eur"],
            current_club_id=row["current_club_id"],
        )
        valuations.append(valuation)
    return valuations


def create_valuations(session: neo4j.Session):
    """
    Creates valuation nodes.
    """
    logger.info("Creating valuation nodes")
    valuations = fetch_valuations()
    for valuation in valuations:
        query = (
            "MATCH (c:Club {club_id: $current_club_id}) "
            "MATCH (p:Player {player_id: $player_id}) "
            "MERGE (p)-[:HAS_VALUATION]->(v:Valuation {date: $date, market_value_in_eur: $market_value_in_eur}) "
        )
        session.run(
            query,
            player_id=valuation.player_id,
            date=valuation.date,
            market_value_in_eur=valuation.market_value_in_eur,
            current_club_id=valuation.current_club_id,
        )

