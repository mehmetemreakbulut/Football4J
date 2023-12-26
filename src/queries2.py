#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""
This query returns the players with the highest goal ratio for 
goals scored for the current club and scored in total.
Return format:
[
    {
        "player_id": "10",
        "player_name": "Miroslav Klose",
        "goal_ratio": 1.0,
        "current_club_name": Società Sportiva Lazio S.p.A.
    }
]
"""

PLAYERS_WITH_HIGHEST_GOAL_RATIO_FOR_THE_CURRENT_CLUB = """
MATCH (p:Player)-[a:APPEARED_IN]->(g:Game)
WITH p, SUM(a.goals) AS total_goals
MATCH (p)-[a_current:APPEARED_IN]->(:Game)
WHERE a_current.player_club_id = p.current_club_id
WITH p, total_goals, SUM(a_current.goals) AS goals_for_current_club
WHERE total_goals > 0 and goals_for_current_club > 0
RETURN p.player_id AS player_id, 
       p.name AS player_name, 
       goals_for_current_club *1.0 / total_goals AS goal_ratio, 
       p.current_club_name AS current_club_name
ORDER BY goal_ratio DESC
"""