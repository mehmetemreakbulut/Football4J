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
        )
        valuations.append(valuation.model_dump())
    return valuations


def create_valuations(session: neo4j.Session):
    """
    Creates valuation nodes.
    """
    valuations = fetch_valuations()
    print(len(valuations))
    for i in range(0, len(valuations)):
        logger.info(f"Creating valuation {i+1}/{len(valuations)}")
        session.run(
            """
            MATCH (p:Player {player_id: $player_id})
            MERGE (p)-[:HAS_VALUATION {date: $date}]->(v:Valuation {market_value_in_eur: $market_value_in_eur})        
            """,
            player_id=valuations[i]["player_id"],
            date=valuations[i]["date"],
            market_value_in_eur=valuations[i]["market_value_in_eur"],
        )





    logger.info("Created valuations")

