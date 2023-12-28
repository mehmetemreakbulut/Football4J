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

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""
This query calculates the total valuation of all players 
in the entire dataset in a monthly basis.
Return format:
[
    {
        "valuationMonth": "2005-01-01",
        "totalValuation": 10000000000
    }
]
"""


TOTAL_VALUATION_OF_ALL_PLAYERS_PER_MONTH = """
WITH date("2005-01-01") AS startDate, // Start date
     date("2023-12-31") AS endDate // End date
WITH startDate, endDate,
     range(startDate.year * 12 + startDate.month - 1, endDate.year * 12 + endDate.month - 1) AS months
UNWIND months AS month
WITH date({year: month / 12, month: month % 12 + 1, day: 1}) AS valuationMonth

MATCH (p:Player)-[r:HAS_VALUATION]->(v:Valuation)
WITH p, v, valuationMonth, r,
     CASE 
         WHEN date(r.date).year < valuationMonth.year OR 
              (date(r.date).year = valuationMonth.year AND date(r.date).month <= valuationMonth.month)
         THEN date(r.date)
         ELSE NULL
     END AS valuationMonthMatch
WHERE valuationMonthMatch IS NOT NULL
WITH valuationMonth, p, MAX(r.date) AS latestValuationDate
MATCH (p)-[r2:HAS_VALUATION {date: latestValuationDate}]->(v2:Valuation)
WITH valuationMonth, SUM(v2.market_value_in_eur) AS totalValuation
RETURN valuationMonth, totalValuation
ORDER BY valuationMonth
"""


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""
This query calculates the total valuation of all players in the entire dataset in a yearly basis.
Return format:
[
    {
        "year": 2005,
        "totalValuation": 10000000000
    }
]
"""

TOTAL_VALUATION_OF_ALL_PLAYERS_PER_YEAR = """
WITH date("2004-01-01") AS startDate, // Start date
     date("2023-12-31") AS endDate // End date
WITH startDate, endDate,
     range(startDate.year, endDate.year) AS years
UNWIND years AS year
WITH date({year: year, month: 1, day: 1}) AS valuationYear

MATCH (p:Player)-[r:HAS_VALUATION]->(v:Valuation)
WITH p, v, valuationYear, r, 
     CASE 
         WHEN date(r.date).year <= valuationYear.year 
         THEN date(r.date).year 
         ELSE NULL 
     END AS valuationYearMatch
WHERE valuationYearMatch IS NOT NULL
WITH valuationYear, p, MAX(r.date) AS latestValuationDate
MATCH (p)-[r2:HAS_VALUATION {date: latestValuationDate}]->(v2:Valuation)
WITH valuationYear.year AS year, SUM(v2.market_value_in_eur) AS totalValuation
RETURN year, totalValuation
ORDER BY year
"""

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

GAMES_PER_SEASON = """
MATCH (g:Game)
WITH g.season AS season, COUNT(g) AS numberOfGames, COLLECT(DISTINCT g.competition_id) AS competitions
RETURN season, 
       numberOfGames, 
       SIZE(competitions) AS numberOfDistinctCompetitions
ORDER BY season
"""

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""
This query calculates the total number of games played per season per club.
Return format:
[
    {
        "season": 2005,
        "numberOfGames": 50,
        "numberOfDistinctCompetitions": 3
    }
]
"""

GAMES_PER_SEASON_PER_CLUB = """
MATCH (c:Club {name: 'Liverpool Football Club'}) 
MATCH (g:Game)
WHERE g.home_club_id = c.club_id OR g.away_club_id = c.club_id
WITH g.season AS season, COUNT(g) AS numberOfGames, COLLECT(DISTINCT g.competition_id) AS competitions
RETURN season, 
       numberOfGames, 
       SIZE(competitions) AS numberOfDistinctCompetitions
ORDER BY season
"""

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

