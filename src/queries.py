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

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the pair clubs that played games with the highest red cards. Find red card from the appearances.
Returns the club1, club2, total_red_cards
Return format:
[
    {
        "club1": "FC Barcelona",
        "club2": "Real Madrid",
        "total_matches": 10,
        "total_red_cards": 10
    }
]
"""

CLUBS_WITH_MOST_RED_CARDS = """
MATCH (c1:Club)<-[:HOME_CLUB|AWAY_CLUB]-(g:Game)-[:HOME_CLUB|AWAY_CLUB]->(c2:Club)
WHERE c1.club_id < c2.club_id and c1.name is not null and c2.name is not null
MATCH (p:Player)-[r:APPEARED_IN]->(g)
RETURN c1.name AS club1, c2.name AS club2, COUNT(DISTINCT g) AS total_matches, SUM(r.red_cards) AS total_red_cards
ORDER BY total_red_cards DESC
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""
This query returns the games with most average value of players. Calculate the average value of players in each game.
Valuation of players is based on the market value of the player in the game.
HAS_VALUATION relationship with closest and a past date is the real valuation of the player in the game.
Returns the game_id, date, club_name, average_market_value_in_eur
"""

GAMES_WITH_MOST_VALUATION = """
MATCH (g:Game)<-[:APPEARED_IN]-(p:Player),
(c_h:Club)<-[:HOME_CLUB]-(g), (c_a:Club)<-[:AWAY_CLUB]-(g)
WHERE c_h.name is not null and c_a.name is not null
WITH g, p, c_h, c_a
CALL {
    WITH g, p
    MATCH (p)-[r:HAS_VALUATION]->(v:Valuation)
    WHERE r.date <= g.date
    RETURN p.player_id AS player_id, g.game_id AS game_id, MAX(r.date) AS max_valuation_date
}
WITH g, p, max_valuation_date, c_h, c_a
MATCH (p)-[r:HAS_VALUATION {date: max_valuation_date}]->(v:Valuation)
RETURN g.date AS game_date, c_h.name AS home_club, c_a.name AS away_club, AVG(v.market_value_in_eur) AS average_valuation
ORDER BY average_valuation DESC
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the referees with their most booked club.
There is a row for each referee. If the referee has booked multiple clubs the most, there will be multiple rows for the referee.
Returns the referee_name, club_name, total_yellow_cards, total_red_cards
Return format:
[
    {
        "referee_name": "Lionel Messi",
        "club_name": "FC Barcelona",
        "total_yellow_cards": 10,
        "total_red_cards": 5
    }
]
"""

REFEREE_MOST_BOOKED_PLAYER = """
MATCH (r:Referee)<-[:REFEREE]-(g:Game)<-[ap:APPEARED_IN]-(p:Player), (c:Club)
WHERE ap.player_club_id = c.club_id 
WITH r, c, SUM(ap.yellow_cards) AS totalYellow, SUM(ap.red_cards) AS totalRed
order by totalYellow+totalRed desc
WITH r, COLLECT({clubName: c.name, yellowCards: totalYellow, redCards: totalRed})[0] AS mostBookedClub
RETURN r.name AS RefereeName, mostBookedClub.clubName AS ClubName, mostBookedClub.yellowCards AS YellowCards, mostBookedClub.redCards AS RedCards
order by YellowCards + RedCards DESC
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the players with lowest minutes played for a goal/asist, in a competition, per season of course.
Only players with more than 450 minutes played are considered. (rougly 5 matches)
Returns the season, competition_id, player_name, minutes_per_goal_or_assist, total_minutes.
"""

PLAYER_GOALS_AND_ASSISTS_PER_MINUTE = """
MATCH (g:Game)<-[ap:APPEARED_IN]-(p:Player),
(comp:Competition)
WHERE g.competition_id = comp.competition_id
WITH g.season AS Season, comp.competition_id AS CompetitionID, p, 
     SUM(ap.goals) AS TotalGoals, SUM(ap.assists) AS TotalAssists, SUM(ap.minutes_played) AS TotalMinutes
WHERE (TotalGoals + TotalAssists)>0 AND TotalMinutes>450
WITH Season, CompetitionID, p, TotalGoals, TotalAssists, TotalMinutes, 
     (TotalMinutes * 1.0) / ((TotalGoals + TotalAssists) * 1.0) AS MinutesPerGA
ORDER BY MinutesPerGA ASC
RETURN Season, CompetitionID, p.name AS PlayerName, MinutesPerGA,TotalMinutes
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the local heros. Players that have highest number of goals/ team's goals in competition and season.
Returns the season, competition_id, player_name, total_goals, total_team_goals, percentage_of_team_goals
"""

PLAYER_LOCAL_HERO = """
MATCH (comp:Competition), 
      (g:Game)-[:COMPETITION]->(comp),
      (c:Club)<-[:HOME_CLUB|AWAY_CLUB]-(g)
where c.name is not null
WITH comp, c, g
// Calculate total goals for each club in the competition and season
WITH comp, c, g.season as season,
     SUM(CASE 
           WHEN g.home_club_id = c.club_id THEN g.home_club_goals 
           WHEN g.away_club_id = c.club_id THEN g.away_club_goals 
           ELSE 0 
         END) AS club_total_goals
// Match players and their goals in the same competition and season
WHERE club_total_goals>20
MATCH (p:Player)-[ap:APPEARED_IN]->(g:Game {season:season})-[:COMPETITION]->(comp), 
      (g)-[:HOME_CLUB|AWAY_CLUB]->(c {club_id: ap.player_club_id})
RETURN p.name, 
       c.name, 
       comp.name, 
       season, 
       SUM(ap.goals) AS goals_by_player, 
       club_total_goals,
       toFloat(SUM(ap.goals))/club_total_goals as ratio
ORDER BY ratio DESC
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the players with most goal+assists for a given country given age range.
Returns the country_name, player_name, total_goals, total_assists, total_minutes_played
"""

PLAYER_GOALS_AND_ASSISTS_FOR_COUNTRY = """
MATCH (p:Player)-[ap:APPEARED_IN]->(g:Game),
      (p)-[:CITIZEN_OF]->(c:Country)
WHERE c.country_name = $country_name
WITH p, ap, g, c,
duration.between(date(p.date_of_birth), date(g.date)).years AS age
WHERE age >= $min_age AND age <= $max_age
RETURN c.country_name AS CountryName, p.name AS PlayerName, SUM(ap.goals) AS TotalGoals, SUM(ap.assists) AS TotalAssists, SUM(ap.minutes_played) AS TotalMinutes
ORDER BY TotalGoals DESC
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
Rate of valuations of players in games to points they get in the game, grouped by each manager.
group by manager name, sum of points from score, sum of valuation at that time

Returns the manager_name, avg_points, total_matches, avg_valuation
"""

MANAGER_POINTS_PER_VALUATION = """
MATCH (g:Game)<-[a:APPEARED_IN]-(p:Player)
MATCH (c_h:Club)<-[:HOME_CLUB]-(g), (c_a:Club)<-[:AWAY_CLUB]-(g)
WHERE c_h.name IS NOT NULL AND c_a.name IS NOT NULL
WITH g, p, c_h, c_a,a

// Find the latest valuation for each player before the game
CALL {
    WITH g, p
    MATCH (p)-[r:HAS_VALUATION]->(v:Valuation)
    WHERE r.date <= g.date
    RETURN p.player_id AS player_id, g.game_id AS game_id, MAX(r.date) AS max_valuation_date
}

WITH g, p, max_valuation_date, c_h, c_a, a
MATCH (p)-[r:HAS_VALUATION {date: max_valuation_date}]->(v:Valuation)

// Aggregate and calculate average valuation for home and away teams
WITH g, 
     c_h.name AS home_club, 
     c_a.name AS away_club, 
     SUM(CASE WHEN a.player_club_id = c_h.club_id THEN v.market_value_in_eur ELSE 0 END) AS home_valuation,
     sum(CASE WHEN a.player_club_id = c_h.club_id THEN 1 ELSE 0 END) as home_player_count,
     SUM(CASE WHEN a.player_club_id = c_a.club_id THEN v.market_value_in_eur ELSE 0 END) AS away_valuation,
     sum(CASE WHEN a.player_club_id = c_a.club_id THEN 1 ELSE 0 END) as away_player_count
WITH g.date AS game_date, 
       home_club, 
       g.home_club_manager_name as home_manager,
       CASE WHEN g.home_club_goals>g.away_club_goals THEN 3 WHEN g.home_club_goals<g.away_club_goals THEN 0 ELSE 1 END as home_club_point,
       away_club, 
       g.away_club_manager_name as away_manager,
       CASE WHEN g.home_club_goals<g.away_club_goals THEN 3 WHEN g.home_club_goals>g.away_club_goals THEN 0 ELSE 1 END as away_club_point,
       home_valuation, 
       home_player_count,
       away_valuation,
       away_player_count
WITH home_manager, home_club_point, CASE WHEN home_player_count > 0 THEN toFloat(home_valuation)/home_player_count else NULL END as home_avg_valuation,
away_manager, away_club_point, CASE WHEN away_player_count > 0 THEN 
toFloat(away_valuation)/away_player_count else NULL END as away_avg_valuation
WITH [{manager: home_manager, point: home_club_point, avg_valuation: home_avg_valuation}, 
     {manager: away_manager, point: away_club_point, avg_valuation: away_avg_valuation}] AS managerList
UNWIND managerList AS managerData
WITH managerData.manager AS manager, managerData.point AS point  , managerData.avg_valuation as average_valuation 
where average_valuation is not null
WITH  manager, avg(point) as avg_point, count(point) as total_matches, avg(average_valuation) as avg_valuation
WHERE total_matches > 30
return manager, avg_point, total_matches, avg_valuation
order by avg_point/log(avg_valuation) desc
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the countries with most average goeal per matches played year by year.
Calculated by (Competition)-[:IN_COUNTRY]->(Country) relationship.
Input is year. Season attribute of Game node is used for year.
Game node has home_club_goals and away_club_goals attributes.

Returns the country_name, total_goals, total_matches, average_goals
"""

COUNTRY_GOALS_PER_MATCH = """
MATCH (g:Game)-[:COMPETITION]->(c:Competition)-[:IN_COUNTRY]->(co:Country)
WHERE g.season = $year
WITH co, g
WITH co, count(g) as total_matches, sum(g.home_club_goals + g.away_club_goals) as total_goals
WHERE total_matches > 0
RETURN co.name as country_name, total_goals, total_matches, toFloat(total_goals)/total_matches as average_goals
ORDER BY average_goals DESC
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the stadiums with most average attendance per matches played year by year.
Also calculate the total red card in the matches played in the stadium.
Calculated by (p:Player)-[ai:APPEARED_IN]->(g:Game)-[:STADIUM]->(s:Stadium) relationship.
ai.red_cards attributes are used for red cards.
Input is year. Season attribute of Game node is used for year.
Game node has attendance attribute.
Returns the 
stadium_name, 
club_name,
total_attendance,
total_matches,
average_attendance,
total_red_cards,
average_red_cards
"""

STADIUM_STAT_PER_MATCH = """
MATCH (g:Game)-[:STADIUM]->(s:Stadium)<-[:HAS_STADIUM]-(c:Club)
where g.season = 2023
WITH s,c, g
MATCH (p:Player)-[ai:APPEARED_IN]->(g)
WITH s,c, g, sum(ai.red_cards) as total_red_cards
WITH s,c, count(g) as total_matches, sum(g.attendance) as total_attendance, sum(total_red_cards) as total_red_cards
WHERE total_matches > 5
RETURN s.name as stadium_name, c.name as club_name, total_attendance, total_matches, toFloat(total_attendance)/total_matches as average_attendance, total_red_cards, toFloat(total_red_cards)/total_matches as average_red_cards
ORDER BY average_red_cards*10  + log10(average_attendance) DESC
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the average point needed to be champion in a competition
Returns the competition_name, average_points
"""

COMPETITION_AVERAGE_POINTS = """
MATCH (comp:Competition)<-[:COMPETITION]-(g:Game),
(c_h:Club)<-[:HOME_CLUB]-(g), (c_a:Club)<-[:AWAY_CLUB]-(g)
WHERE c_h.name IS NOT NULL AND c_a.name IS NOT NULL and EXISTS(()-[:HAS_DOMESTIC_COMPETITION]->(comp))
WITH g, comp.name as comp,
     c_h.name AS home_club, 
     c_a.name AS away_club
WITH g.date AS game_date, g.season as season, comp,
       home_club, 
       CASE WHEN g.home_club_goals>g.away_club_goals THEN 3 WHEN g.home_club_goals<g.away_club_goals THEN 0 ELSE 1 END as home_club_point,
       away_club, 
       CASE WHEN g.home_club_goals<g.away_club_goals THEN 3 WHEN g.home_club_goals>g.away_club_goals THEN 0 ELSE 1 END as away_club_point
WITH [{name: home_club, point: home_club_point, season: season, comp:comp}, 
     {name: away_club, point: away_club_point, season: season,comp:comp}] AS clubList
UNWIND clubList as club
with club.season as season, club.comp as competition, club.name as club_name, club.point as point
with season, competition, club_name, sum(point) as total_point
order by total_point desc
with distinct season, competition, collect(club_name) as clubs, collect(total_point) as points
WITH season, competition, clubs[0] as club, points[0] as point
RETURN competition, avg(point) as average_champion_point
order by average_champion_point desc
"""


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



"""
This query returns the average goal difference for each coach in a given year.

Returns the manager_name, average_goal_difference"""

MANAGER_AVERAGE_GOAL_DIFFERENCE = """
MATCH (g:Game)<-[a:APPEARED_IN]-(p:Player)
MATCH (c_h:Club)<-[:HOME_CLUB]-(g), (c_a:Club)<-[:AWAY_CLUB]-(g)
WHERE c_h.name IS NOT NULL AND c_a.name IS NOT NULL and g.season = $year
WITH g, p, c_h, c_a,a
// Find the latest valuation for each player before the game
CALL {
    WITH g, p
    MATCH (p)-[r:HAS_VALUATION]->(v:Valuation)
    WHERE r.date <= g.date
    RETURN p.player_id AS player_id, g.game_id AS game_id, MAX(r.date) AS max_valuation_date
}

WITH g, p, max_valuation_date, c_h, c_a, a
MATCH (p)-[r:HAS_VALUATION {date: max_valuation_date}]->(v:Valuation)

// Aggregate and calculate average valuation for home and away teams
WITH g, 
     c_h.name AS home_club, 
     c_a.name AS away_club
WITH g.date AS game_date, 
       home_club, 
       g.home_club_manager_name as home_manager,
       g.home_club_goals as home_club_goals,
       away_club, 
       g.away_club_manager_name as away_manager,
       g.away_club_goals as away_club_goals
WITH [{manager: home_manager, goals_scored: home_club_goals, goals_conceded: away_club_goals}, 
     {manager: away_manager, goals_scored: away_club_goals, goals_conceded: home_club_goals}] AS managerList
UNWIND managerList AS managerData
WITH managerData.manager AS manager, managerData.goals_scored AS goals_scored  , managerData.goals_conceded as goals_conceded
WITH goals_scored - goals_conceded as goal_difference, manager
WITH  manager, avg(goal_difference) as average_goal_difference, count(goal_difference) as total_matches
WHERE total_matches > 30
return manager, average_goal_difference, total_matches
order by average_goal_difference desc
"""



# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the average valuation of players in a given year for each country.
"""

COUNTRY_AVERAGE_VALUATION = """
MATCH (p:Player)-[r:HAS_VALUATION]->(v:Valuation)
WITH p, v
WHERE duration.between(date(r.date), date({year:$average, month: 12, day:31})).months < 12
CALL {
    WITH p
    MATCH (p)-[r:HAS_VALUATION]->(v:Valuation)
    RETURN p.player_id AS player_id, MAX(r.date) AS max_valuation_date
}
WITH p, max_valuation_date
MATCH (p)-[r:HAS_VALUATION {date: max_valuation_date}]->(v_n:Valuation)
WITH distinct p, collect(v_n)[0] as v_n
MATCH (p)-[:CITIZEN_OF]->(c:Country)
WITH c, v_n
WITH c.country_name AS country_name, AVG(v_n.market_value_in_eur) AS average_valuation, count(v_n) as total_players
WHERE total_players > 5
return *
ORDER BY average_valuation  DESC
"""







