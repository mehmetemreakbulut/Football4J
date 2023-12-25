import logging
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

from src.models.appearances import create_appearances
from src.models.player import create_players
from src.models.club import create_clubs
from src.models.game import create_games
from src.models.competition import create_competitions
from src.models.valuation import create_valuations

load_dotenv()

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

NODE_CREATION_PIPELINE = [
    create_competitions,
    create_clubs,
    create_players,
    create_games,
]

RELATIONSHIP_CREATION_PIPELINE = [
    create_appearances,
    #create_valuations,
]


def run_pipeline():
    with GraphDatabase.driver(os.getenv("NEO4J_URL"),
                              auth=(os.getenv("NEO4J_USER"),
                                    os.getenv("NEO4J_PASSWORD"))) as driver:
        with driver.session() as session:
            for step in NODE_CREATION_PIPELINE:
                continue
                step(session)
            for step in RELATIONSHIP_CREATION_PIPELINE:
                step(session)


if __name__ == "__main__":
    run_pipeline()
