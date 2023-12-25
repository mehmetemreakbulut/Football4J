"""
This file contains all the queries that are used in the application.

The queries are stored in a dictionary, where the key is the name of the query and the value is the query itself.

The queries are stored in a separate file to make it easier to read the code in the other files.

"""

"""
This query returns the players and their appearances grouped by competition and club.
If he has played in multiple clubs in the given competition, there will be multiple rows for the player.
Returns the player_id, player_name, club_name, total_appearances, total_goals, total_assists, total_yellow_cards, total_red_cards, total_minutes_played,
Return format:
[
    {
        "player_id": 1,
        "player_name": "Lionel Messi",
        "club_name": "FC Barcelona",
        "total_appearances": 10,
        "total_goals": 5,
        "total_assists": 3,
        "total_yellow_cards": 2,
        "total_red_cards": 0,
        "total_minutes_played": 900
    }
]
"""
PLAYER_APPEARANCES_IN_COMPETITION = """
MATCH (p:Player)-[r:APPEARED_IN]->(g:Game)
MATCH (competition:Competition {name: $competition_name})
WHERE g.competition_id = competition.competition_id
MATCH (g)-[:HOME_CLUB|AWAY_CLUB]->(c:Club {club_id: r.player_club_id})
RETURN p.player_id AS player_id, p.name AS player_name, c.name AS club_name,
COUNT(r) AS total_appearances, SUM(r.goals) AS total_goals, SUM(r.assists) AS total_assists,
SUM(r.yellow_cards) AS total_yellow_cards, SUM(r.red_cards) AS total_red_cards, SUM(r.minutes_played) AS total_minutes_played
ORDER BY total_appearances DESC
"""



