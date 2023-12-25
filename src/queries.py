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
MATCH (p:Player)-[r:APPEARED_IN]->(g:Game)-[:HOME_CLUB|AWAY_CLUB]->(c:Club {club_id: r.player_club_id}),
(competition:Competition {name: $competition_name})
WHERE g.competition_id = competition.competition_id and c.name is not null
RETURN p.player_id AS player_id, p.name AS player_name, c.name AS club_name,
COUNT(r) AS total_appearances, SUM(r.goals) AS total_goals, SUM(r.assists) AS total_assists,
SUM(r.yellow_cards) AS total_yellow_cards, SUM(r.red_cards) AS total_red_cards, SUM(r.minutes_played) AS total_minutes_played
ORDER BY total_appearances DESC
"""



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the players and their goals and asists grouped by against club.
If he has played against multiple clubs, there will be multiple rows for the player.
Returns the player_id, player_name, against_club_name, total_goals, total_assists
Return format:
[
    {
        "player_id": 1,
        "player_name": "Lionel Messi",
        "own_club_name": "FC Barcelona",
        "against_club_name": "Real Madrid",
        "total_goals": 5,
        "total_assists": 3
    }
]
"""

PLAYER_GOALS_AND_ASSISTS_AGAINST_CLUB = """
MATCH (p:Player)-[r:APPEARED_IN]->(g:Game)-[:HOME_CLUB|AWAY_CLUB]->(c: Club {club_id: r.player_club_id}), 
(g)-[:HOME_CLUB|AWAY_CLUB]->(against_club: Club)
WHERE against_club.club_id <> c.club_id and c.name is not null and against_club.name is not null
RETURN p.player_id AS player_id, p.name AS player_name, c.name AS own_club_name, against_club.name AS against_club_name,
SUM(r.goals) AS total_goals, SUM(r.assists) AS total_assists
ORDER BY total_goals DESC
"""


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



"""
This query return the players which played against each other the most.
Returns the player_id, player_1_name, player_2_name, total_appearances
Return format:
[
    {
        "player_id": 1,
        "player_1_name": "Lionel Messi",
        "player_2_name": "Cristiano Ronaldo",
        "total_appearances": 10
    }
]
"""
PLAYER_AGAINST_PLAYER = """
MATCH (p1:Player)-[r1:APPEARED_IN]->(g:Game)<-[r2:APPEARED_IN]-(p2:Player),
(competition:Competition {name: $competition_name})
WHERE p1.player_id < p2.player_id and r1.player_club_id <> r2.player_club_id and 
WHERE g.competition_id = competition.competition_id
RETURN p1.player_id AS player_1_id, p1.name AS player_1_name, p2.player_id AS player_2_id, p2.name AS player_2_name,
COUNT(r1) AS total_appearances
ORDER BY total_appearances DESC
"""



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



"""
This query returns the leagues and the number of players that have played in the league and the average age of the players in the games played, calculated from the date of the game minus the date of birth of the player.
Returns the competition_id, competition_name, total_players, average_age
Return format:
[
    {
        "competition_id": 1,
        "competition_name": "La Liga",
        "total_players": 100,
        "average_age": 25
    }
]
"""
LEAGUE_PLAYERS_AND_AGE = """
MATCH (p:Player)-[r:APPEARED_IN]->(g:Game)-[:COMPETITION]->(c:Competition)
WHERE c.name IS NOT NULL
WITH c, p, g, r,
     duration.between(date(p.date_of_birth), date(g.date)).years AS age
RETURN c.competition_id AS competition_id, c.name AS competition_name,
       COUNT(DISTINCT p) AS total_players, toInteger(avg(age)) AS average_age
ORDER BY average_age DESC
"""


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""
This query returns the players that got most win against a club.
Returns the player_id, player_name, club_name, against_club_name, total_wins, total_losses, total_draws
Return format:
[
    {
        "player_id": 1,
        "player_name": "Lionel Messi",
        "club_name": "FC Barcelona",
        "against_club_name": "Real Madrid",
        "total_wins": 10,
        "total_losses": 5,
        "total_draws": 3
    }
]
"""
PLAYER_WINS_AGAINST_HIGHER_POSITION_CLUB = """
MATCH (p:Player)-[r:APPEARED_IN]->(g:Game)-[:HOME_CLUB|AWAY_CLUB]->(c:Club {club_id: r.player_club_id}),
(g)-[:HOME_CLUB|AWAY_CLUB]->(against_club: Club),
(competition:Competition {name: $competition_name})
WHERE g.competition_id = competition.competition_id 
RETURN p.player_id AS player_id, p.name AS player_name, c.name AS club_name, against_club.name AS against_club_name,
SUM(CASE WHEN g.home_club_goals > g.away_club_goals and c.club_id = g.home_club_id THEN 1
            WHEN g.away_club_goals > g.home_club_goals and c.club_id = g.away_club_id THEN 1
            ELSE 0 END) AS total_wins,
SUM(CASE WHEN g.home_club_goals < g.away_club_goals and c.club_id = g.home_club_id THEN 1
            WHEN g.away_club_goals < g.home_club_goals and c.club_id = g.away_club_id THEN 1
            ELSE 0 END) AS total_losses,
SUM(CASE WHEN g.home_club_goals = g.away_club_goals THEN 1 ELSE 0 END) AS total_draws
ORDER BY total_wins DESC
"""









