import logging
from typing import Optional

import neo4j
import numpy as np
from pydantic import BaseModel
import pandas as pd
from ..constants import SOURCE_FOLDER

logger = logging.getLogger(__name__)


class Player(BaseModel):
    player_id: int
    first_name: Optional[str] = None
    last_name: str
    name: str
    last_season: int
    current_club_id: int
    player_code: str
    country_of_birth: Optional[str] = None
    city_of_birth: Optional[str] = None
    country_of_citizenship: Optional[str] = None
    date_of_birth: Optional[str] = None
    sub_position: Optional[str] = None
    position: str
    foot: Optional[str] = None
    height_in_cm: Optional[int] = None
    contract_expiration_date: Optional[str] = None
    agent_name: Optional[str] = None
    image_url: str
    url: str
    current_club_domestic_competition_id: str
    current_club_name: str
    market_value_in_eur: Optional[int] = None
    highest_market_value_in_eur: Optional[int] = None


def fetch_players():
    """
    Fetches players from SOURCE_PATH and returns a list of Player objects.
    """
    df = pd.read_csv(SOURCE_FOLDER + "/players.csv", sep=",")
    df = df.replace({np.nan: None})
    players = []
    for index, row in df.iterrows():
        player = Player(
            player_id=row["player_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            name=row["name"],
            last_season=row["last_season"],
            current_club_id=row["current_club_id"],
            player_code=row["player_code"],
            country_of_birth=row["country_of_birth"],
            city_of_birth=row["city_of_birth"],
            country_of_citizenship=row["country_of_citizenship"],
            date_of_birth=row["date_of_birth"],
            sub_position=row["sub_position"],
            position=row["position"],
            foot=row["foot"],
            height_in_cm=row["height_in_cm"],
            contract_expiration_date=row["contract_expiration_date"],
            agent_name=row["agent_name"],
            image_url=row["image_url"],
            url=row["url"],
            current_club_domestic_competition_id=row["current_club_domestic_competition_id"],
            current_club_name=row["current_club_name"],
            market_value_in_eur=row["market_value_in_eur"],
            highest_market_value_in_eur=row["highest_market_value_in_eur"]
        )
        players.append(player)
    return players


def create_player_constraints(neo4j_session: neo4j.Session):
    with neo4j_session.begin_transaction() as tx:
        tx.run("CREATE CONSTRAINT IF NOT EXISTS  FOR (p:Player) REQUIRE p.player_id IS UNIQUE;")

        tx.run("CREATE INDEX IF NOT EXISTS  FOR (p:Player) ON (p.name);")
        tx.commit()


def create_players(neo4j_session: neo4j.Session):
    create_player_constraints(neo4j_session)
    with neo4j_session.begin_transaction() as tx:
        for player in fetch_players():
            tx.run(
                """
                MERGE (p:Player {player_id: $player_id})
                ON CREATE SET p.first_name = $first_name,
                              p.last_name = $last_name,
                              p.name = $name,
                              p.last_season = $last_season,
                              p.current_club_id = $current_club_id,
                              p.player_code = $player_code,
                              p.country_of_birth = $country_of_birth,
                              p.city_of_birth = $city_of_birth,
                              p.country_of_citizenship = $country_of_citizenship,
                              p.date_of_birth = $date_of_birth,
                              p.sub_position = $sub_position,
                              p.position = $position,
                              p.foot = $foot,
                              p.height_in_cm = $height_in_cm,
                              p.contract_expiration_date = $contract_expiration_date,
                              p.agent_name = $agent_name,
                              p.image_url = $image_url,
                              p.url = $url,
                              p.current_club_domestic_competition_id = $current_club_domestic_competition_id,
                              p.current_club_name = $current_club_name,
                              p.market_value_in_eur = $market_value_in_eur,
                              p.highest_market_value_in_eur = $highest_market_value_in_eur
                """,
                player_id=player.player_id,
                first_name=player.first_name,
                last_name=player.last_name,
                name=player.name,
                last_season=player.last_season,
                current_club_id=player.current_club_id,
                player_code=player.player_code,
                country_of_birth=player.country_of_birth,
                city_of_birth=player.city_of_birth,
                country_of_citizenship=player.country_of_citizenship,
                date_of_birth=player.date_of_birth,
                sub_position=player.sub_position,
                position=player.position,
                foot=player.foot,
                height_in_cm=player.height_in_cm,
                contract_expiration_date=player.contract_expiration_date,
                agent_name=player.agent_name,
                image_url=player.image_url,
                url=player.url,
                current_club_domestic_competition_id=player.current_club_domestic_competition_id,
                current_club_name=player.current_club_name,
                market_value_in_eur=player.market_value_in_eur,
                highest_market_value_in_eur=player.highest_market_value_in_eur
            )

            tx.run(
                """
                MATCH (p:Player {player_id: $player_id})
                MATCH (c:Club {club_id: $club_id})
                MERGE (p)-[r:CURRENT_CLUB]->(c)
                """,
                player_id=player.player_id,
                club_id=player.current_club_id,
            )

        tx.commit()

        logger.info("Created player nodes")
