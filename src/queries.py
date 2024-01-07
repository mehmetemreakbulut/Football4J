"""
This file contains all the queries that are used in the application.

The queries are stored in a dictionary, where the key is the name of the query and the value is the query itself.

The queries are stored in a separate file to make it easier to read the code in the other files.

"""

"""
This query returns the players and their appearances grouped by competition and club.
If he has played in multiple clubs in the given competition, there will be multiple rows for the player.
Returns the Player_ID, Player_Name, Club_Name, Appereances, Goals_Scored, Assists, Yellow_Cards, Red_Cards, Minutes_Played
Return format:
[
    {
        "Player_ID": 1,
        "Player_Name": "Lionel Messi",
        "Club_Name": "FC Barcelona",
        "Appereances": 10,
        "Goals_Scored": 5,
        "Assists": 3,
        "Yellow_Cards": 2,
        "Red_Cards": 0,
        "Minutes_Played": 900
    }
]
"""
PLAYER_APPEARANCES_IN_COMPETITION = """
MATCH (p:Player)-[r:APPEARED_IN]->(g:Game)-[:HOME_CLUB|AWAY_CLUB]->(c:Club {club_id: r.player_club_id}),
(competition:Competition {name: "laliga"})
WHERE g.competition_id = competition.competition_id and c.name is not null
RETURN p.player_id AS Player_ID, p.name AS Player_Name, c.name AS Club_Name,
COUNT(r) AS Appereances, SUM(r.goals) AS Goals_Scored, SUM(r.assists) AS Assists,
SUM(r.yellow_cards) AS Yellow_Cards, SUM(r.red_cards) AS Red_Cards, SUM(r.minutes_played) AS Minutes_Played
ORDER BY Appereances DESC
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the players and their goals and asists grouped by against club.
If he has played against multiple clubs, there will be multiple rows for the player.
Returns the Player_ID, Player_Name, Own_Club_Name, Against_Club_Name, Goals_Scored, Assists
Return format:
[
    {
        "Player_ID": 1,
        "Player_Name": "Lionel Messi",
        "Own_Club_Name": "FC Barcelona",
        "Against_Club_Name": "Real Madrid",
        "Goals_Scored": 5,
        "Assists": 3
    }
]
"""

PLAYER_GOALS_AND_ASSISTS_AGAINST_CLUB = """
MATCH (p:Player)-[r:APPEARED_IN]->(g:Game)-[:HOME_CLUB|AWAY_CLUB]->(c: Club {club_id: r.player_club_id}), 
(g)-[:HOME_CLUB|AWAY_CLUB]->(against_club: Club)
WHERE against_club.club_id <> c.club_id and c.name is not null and against_club.name is not null
WITH p.player_id AS Player_ID, p.name AS Player_Name, c.name AS Own_Club_Name, against_club.name AS Against_Club_Name,
SUM(r.goals) AS Goals_Scored, SUM(r.assists) AS Assists
WHERE Goals_Scored > 0
RETURN Player_ID, Player_Name, Own_Club_Name, Against_Club_Name, Goals_Scored, Assists
ORDER BY Goals_Scored DESC, Assists DESC
LIMIT(1000)
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query return the players which played against each other the most.
Returns the Player_1_ID, Player_1_Name, player_2_id, Player_2_Name, Appereances_Against
Return format:
[
    {
        "Player_1_ID": 1,
        "Player_1_Name": "Lionel Messi",
        "player_2_id": 2,
        "Player_2_Name": "Cristiano Ronaldo",
        "Appereances_Against": 10
    }
]
"""
PLAYER_AGAINST_PLAYER = """
MATCH (p1:Player)-[r1:APPEARED_IN]->(g:Game)<-[r2:APPEARED_IN]-(p2:Player),
(competition:Competition {name: 'laliga'})
WHERE p1.player_id < p2.player_id and r1.player_club_id <> r2.player_club_id and g.competition_id = competition.competition_id
RETURN p1.player_id AS Player_1_ID, p1.name AS Player_1_Name, p2.player_id AS player_2_id, p2.name AS Player_2_Name,
COUNT(r1) AS Appereances_Against
ORDER BY Appereances_Against DESC
LIMIT(1000)
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the leagues and the number of players that have played in the league and the average age of the players in the games played, calculated from the date of the game minus the date of birth of the player.
Returns the Competition_ID, Competition_Name, Total_Number_of_Players, Average_Age
Return format:
[
    {
        "Competition_ID": 1,
        "Competition_Name": "La Liga",
        "Total_Number_of_Players": 100,
        "Average_Age": 25
    }
]
"""
LEAGUE_PLAYERS_AND_AGE = """
MATCH (p:Player)-[r:APPEARED_IN]->(g:Game)-[:PLAYED_FOR]->(c:Competition)
WHERE c.name IS NOT NULL
WITH c, p, g, r, duration.between(date(p.date_of_birth), date(g.date)).years AS age
RETURN c.competition_id AS Competition_ID, c.name AS Competition_Name, COUNT(DISTINCT p) AS Total_Number_of_Players, toInteger(avg(age)) AS Average_Age
ORDER BY Average_Age DESC
LIMIT(1000)
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""
This query returns the players that got most win against a club.
Returns the Player_ID, Player_Name, Own_Club_Name, Against_Club_name, Wins, Losses, Draws
Return format:
[
    {
        "Player_ID": 1,
        "Player_Name": "Lionel Messi",
        "Own_Club_Name": "FC Barcelona",
        "Against_Club_name": "Real Madrid",
        "Wins": 10,
        "Losses": 5,
        "Draws": 3
    }
]
"""
PLAYER_WINS_AGAINST_HIGHER_POSITION_CLUB = """
MATCH (p:Player)-[r:APPEARED_IN]->(g:Game)-[:HOME_CLUB|AWAY_CLUB]->(c:Club {club_id: r.player_club_id}),
(g)-[:HOME_CLUB|AWAY_CLUB]->(against_club: Club),
(competition:Competition {name: 'laliga'})
WHERE g.competition_id = competition.competition_id 
RETURN p.player_id AS Player_ID, p.name AS Player_Name, c.name AS Own_Club_Name, against_club.name AS Against_Club_name,
SUM(CASE WHEN g.home_club_goals > g.away_club_goals and c.club_id = g.home_club_id THEN 1
            WHEN g.away_club_goals > g.home_club_goals and c.club_id = g.away_club_id THEN 1
            ELSE 0 END) AS Wins,
SUM(CASE WHEN g.home_club_goals < g.away_club_goals and c.club_id = g.home_club_id THEN 1
            WHEN g.away_club_goals < g.home_club_goals and c.club_id = g.away_club_id THEN 1
            ELSE 0 END) AS Losses,
SUM(CASE WHEN g.home_club_goals = g.away_club_goals THEN 1 ELSE 0 END) AS Draws
ORDER BY Wins DESC, Losses ASC, Draws DESC
LIMIT(1000)
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the pair clubs that played games with the highest red cards. Find red card from the appearances.
Returns the Club_1_Name, Club_2_Name, Red_Cards
Return format:
[
    {
        "Club_1_Name": "FC Barcelona",
        "Club_2_Name": "Real Madrid",
        "Matches_Played": 10,
        "Red_Cards": 10
    }
]
"""

CLUBS_WITH_MOST_RED_CARDS = """
MATCH (c1:Club)<-[:HOME_CLUB|AWAY_CLUB]-(g:Game)-[:HOME_CLUB|AWAY_CLUB]->(c2:Club)
WHERE c1.club_id < c2.club_id and c1.name is not null and c2.name is not null
MATCH (p:Player)-[r:APPEARED_IN]->(g)
RETURN c1.name AS Club_1_Name, c2.name AS Club_2_Name, COUNT(DISTINCT g) AS Matches_Played, SUM(r.red_cards) AS Red_Cards
ORDER BY Red_Cards DESC, Matches_Played ASC
LIMIT(1000)
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""
This query returns the games with most average value of players. Calculate the average value of players in each game.
Valuation of players is based on the market value of the player in the game. HAS_VALUATION relationship with closest and a past date is the real valuation of the player in the game.
Returns the Date, Home_Club, Away_Club, Average_Valuation_of_Players.

Return format:
[
    {
        "Date": "FC Barcelona",
        "Home_Club": "Real Madrid",
        "Away_Club": 10,
        "Average_Valuation_of_Players": 10
    }
]
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
RETURN g.date AS Date, c_h.name AS Home_Club, c_a.name AS Away_Club, ROUND(AVG(v.market_value_in_eur)) AS Average_Valuation_of_Players
ORDER BY Average_Valuation_of_Players DESC
LIMIT(1000)
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the referees with their most booked club.
There is a row for each referee. If the referee has booked multiple clubs the most, there will be multiple rows for the referee.
Returns the Referee_Name, Club_Name, Yellow_Cards, Red_Cards
Return format:
[
    {
        "Referee_Name": "Lionel Messi",
        "Club_Name": "FC Barcelona",
        "Yellow_Cards": 10,
        "Red_Cards": 5
    }
]
"""

REFEREE_MOST_BOOKED_PLAYER = """
MATCH (r:Referee)<-[:REFEREE]-(g:Game)<-[ap:APPEARED_IN]-(p:Player), (c:Club)
WHERE ap.player_club_id = c.club_id 
WITH r, c, SUM(ap.yellow_cards) AS totalYellow, SUM(ap.red_cards) AS totalRed
order by totalYellow+totalRed desc
WITH r, COLLECT({clubName: c.name, yellowCards: totalYellow, redCards: totalRed})[0] AS mostBookedClub
RETURN r.name AS Referee_Name, mostBookedClub.clubName AS Club_Name, mostBookedClub.yellowCards AS Yellow_Cards, mostBookedClub.redCards AS Red_Cards
order by Yellow_Cards + Red_Cards DESC, Red_Cards DESC, Yellow_Cards DESC
LIMIT(1000)
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the players with lowest minutes played for a goal/asist, in a competition, per season of course.
Only players with more than 450 minutes played are considered. (rougly 5 matches)
Returns the Season, Competition_ID, Player_Name, Minutes_Per_Contibution, Total_Minutes.

Return format:
[
    {
        "Season": "2019",
        "Competition_ID": "CL",
        "Player_Name": "Rpbert Lewandowski",
        "Minutes_Per_Contibution": 42,
        "Total_Minutes": 450
    }
]


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
RETURN Season, CompetitionID as Competition_ID, p.name AS Player_Name, ROUND(MinutesPerGA) as Minutes_Per_Contibution,TotalMinutes as Total_Minutes
LIMIT(1000)
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the local heros. Players that have highest number of goals / team's goals in competition and season.
Returns the Player_Name, Club_Name, Competition_Name, Season, Goals_Scored_By_Player, Total_Club_Goals, Goals_Scored, Ratio

Return format:
[
    {
        "Player_Name": "Lionel Messi",
        "Club_Name": "FC Barcelona",
        "Competition_Name": "La Liga",
        "Season": "2019",
        "Goals_Scored_By_Player": 30,
        "Total_Club_Goals": 40,
        "Ratio": 0.75
    }
]
"""

PLAYER_LOCAL_HERO = """
MATCH (comp:Competition), 
      (g:Game)-[:PLAYED_FOR]->(comp),
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
MATCH (p:Player)-[ap:APPEARED_IN]->(g:Game {season:season})-[:PLAYED_FOR]->(comp), 
      (g)-[:HOME_CLUB|AWAY_CLUB]->(c {club_id: ap.player_club_id})
RETURN p.name as Player_Name, 
       c.name as Club_Name, 
       comp.name as Competition_Name, 
       season as Season, 
       SUM(ap.goals) AS Goals_Scored_By_Player, 
       club_total_goals as Total_Club_Goals,
       ROUND(toFloat(SUM(ap.goals))/club_total_goals, 4) as Ratio
ORDER BY Ratio DESC
LIMIT(1000)
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the players with most goal+assists for a given country and given age range.
Returns the Country_Name, Player_Name, Goals_Scored, Assists, Minutes_Played

Return format:
[
    {
        "Country_Name": "Argentina",
        "Player_Name": "Lionel Messi",
        "Goals_Scored": 30,
        "Assists": 20,
        "Minutes_Played": 4500
    }
]

"""

PLAYER_GOALS_AND_ASSISTS_FOR_COUNTRY = """
MATCH (p:Player)-[ap:APPEARED_IN]->(g:Game),
      (p)-[:CITIZEN_OF]->(c:Country)
WHERE c.country_name = 'Italy'
WITH p, ap, g, c,
duration.between(date(p.date_of_birth), date(g.date)).years AS age
WHERE age >= 15 AND age <= 40
RETURN c.country_name AS Country_Name, p.name AS Player_Name, SUM(ap.goals) AS Goals_Scored, SUM(ap.assists) AS Assists, SUM(ap.minutes_played) AS Minutes_Played
ORDER BY Goals_Scored DESC, Assists DESC, Minutes_Played ASC
LIMIT(1000)
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
Rate of valuations of players in games to points they get in the game, grouped by each manager. This query calculates the success of the manager. The higher the score, the better the manager.
Group by manager name, sum of points from score, sum of valuation at that time

Returns the Manager, Average_Point, Matches_Played, Average_Valuation, Score

Return format:
[
    {
        "Manager": "Lionel Messi",
        "Average_Point": 1.5,
        "Matches_Played": 100,
        "Average_Valuation": 1000000000,
        "Score": 0.5
    }
]
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
WITH  manager, avg(point) as avg_point, count(point) as Matches_Played, avg(average_valuation) as avg_valuation
WHERE Matches_Played > 30
return manager as Manager, Round(avg_point,1) as Average_Point, Matches_Played as Matches_Played, ROUND(avg_valuation) as Average_Valuation, ROUND(avg_point/log(avg_valuation)*65, 5) as Score
order by Score desc
limit(1000)
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the countries with most average goal per matches played year by year.
Calculated by (Competition)-[:IN_COUNTRY]->(Country) relationship.
Input is year. Season attribute of Game node is used for year.
Game node has home club goals and away club goals attributes.

Returns the Country_Name, Goals_Scored, Matches_Played, Average_Goals

Return format:
[
    {
        "Country_Name": "Argentina",
        "Goals_Scored": 10,
        "Matches_Played": 5,
        "Average_Goals": 2
    }
]
"""

COUNTRY_GOALS_PER_MATCH = """
MATCH (g:Game)-[:PLAYED_FOR]->(c:Competition)-[:IN_COUNTRY]->(co:Country)
WHERE g.season = 2016
WITH co, g
WITH co, count(g) as Matches_Played, sum(g.home_club_goals + g.away_club_goals) as Goals_Scored
WHERE Matches_Played > 0
RETURN co.name as Country_Name, Goals_Scored as Goals_Scored, Matches_Played as Matches_Played, round(toFloat(Goals_Scored)/Matches_Played, 2) as Average_Goals
ORDER BY Average_Goals DESC, Goals_Scored DESC, Matches_Played ASC
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the stadiums with most average attendance per matches played year by year.
Also calculate the total red card in the matches played in the stadium.
Calculated by (p:Player)-[ai:APPEARED_IN]->(g:Game)-[:PLAYED_IN]->(s:Stadium) relationship.
ai.red_cards attributes are used for red cards.
Input is year. Season attribute of Game node is used for year.
Game node has attendance attribute.

Returns the 
Stadium, 
Club,
Total_Attendance,
Matches_Played,
Average_Attendance,
Red_Cards,
Average_Red_Cards,
Score

Return format:
[
    {
        "Stadium": "Camp Nou",
        "Club": "FC Barcelona",
        "Total_Attendance": 100000,
        "Matches_Played": 10,
        "Average_Attendance": 10000,
        "Red_Cards": 10,
        "Average_Red_Cards": 1,
        "Score": 10
    }
]

"""

STADIUM_STAT_PER_MATCH = """
MATCH (g:Game)-[:PLAYED_IN]->(s:Stadium)<-[:HAS_STADIUM]-(c:Club)
where g.season = 2023
WITH s,c, g
MATCH (p:Player)-[ai:APPEARED_IN]->(g)
WITH s,c, g, sum(ai.red_cards) as Red_Cards
WITH s,c, count(g) as Matches_Played, sum(g.attendance) as total_attendance, sum(Red_Cards) as Red_Cards
WHERE Matches_Played > 5
WITH s.name as Stadium, c.name as Club, total_attendance as Total_Attendance, Matches_Played as Matches_Played, round(toFloat(total_attendance)/Matches_Played, 1) as Average_Attendance, Red_Cards as Red_Cards, round(toFloat(Red_Cards)/Matches_Played, 2) as Average_Red_Cards
WHERE Average_Attendance>0
RETURN Stadium, Club, Total_Attendance, Matches_Played, Average_Attendance, Red_Cards, Average_Red_Cards,
(Average_Red_Cards*10  + log10(Average_Attendance)) as Score
ORDER BY Score DESC
"""

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the average point needed to be champion in a competition.
Returns the Competition, Average_Championship_Point

Return format:
[
    {
        "Competition": "La Liga",
        "Average_Championship_Point": 80
    }
]
"""

COMPETITION_AVERAGE_POINTS = """
MATCH (comp:Competition)<-[:PLAYED_FOR]-(g:Game),
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
RETURN competition as Competition, round(avg(point),2) as Average_Championship_Point
order by Average_Championship_Point desc
"""


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



"""
This query returns the average goal difference for each coach in a given year.

Returns the Manager, Average_Goal_Difference, Matches_Played


Return format:
[
    {
        "Manager": "Lionel Messi",
        "Average_Goal_Difference": 1.5,
        "Matches_Played": 100
    }
]
"""

MANAGER_AVERAGE_GOAL_DIFFERENCE = """
MATCH (g:Game)<-[a:APPEARED_IN]-(p:Player)
MATCH (c_h:Club)<-[:HOME_CLUB]-(g), (c_a:Club)<-[:AWAY_CLUB]-(g)
WHERE c_h.name IS NOT NULL AND c_a.name IS NOT NULL and g.season = 2017
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
WITH  manager, avg(goal_difference) as average_goal_difference, count(goal_difference) as Matches_Played
WHERE Matches_Played > 30
return manager as Manager, round(average_goal_difference, 2) as Average_Goal_Difference, Matches_Played as Matches_Played
order by Average_Goal_Difference desc, Matches_Played asc
"""



# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


"""
This query returns the average valuation of players in a given year for each country.
Returns the Country_Name, Average_Valuation, Total_Players

Return format:
[
    {
        "Country_Name": "Argentina",
        "Average_Valuation": 1000000,
        "Number_of_Players": 100
    }
]
"""

COUNTRY_AVERAGE_VALUATION = """
MATCH (p:Player)-[r:HAS_VALUATION]->(v:Valuation)
WITH p, v
WHERE duration.between(date(r.date), date({year:2005, month: 12, day:31})).months < 12
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
return country_name as Country_Name, total_players as Number_of_Players, round(average_valuation) as Average_Valuation
ORDER BY Average_Valuation  DESC
"""


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""
This query returns the players with the highest goal ratio for goals scored for the current club and scored in total.
Returns the Player_ID, Player_Name, Latest_Club, Goals_For_Latest_Club, Goals_Scored, Goal_Ratio


Return format:
[
    {
        "Player_ID": 1,
        "Player_Name": "Lionel Messi",
        "Latest_Club": "FC Barcelona",
        "Goals_For_Latest_Club": 190,
        "Goals_Scored": 200,
        "Goal_Ratio": 0.95
    }
]
"""

PLAYERS_WITH_HIGHEST_GOAL_RATIO_FOR_THE_CURRENT_CLUB = """
MATCH (p:Player)-[a:APPEARED_IN]->(g:Game)
WITH p, SUM(a.goals) AS Goals_Scored
MATCH (p)-[a_current:APPEARED_IN]->(:Game)
WHERE a_current.player_club_id = p.current_club_id
WITH p, Goals_Scored, SUM(a_current.goals) AS goals_for_current_club
WHERE Goals_Scored > 20 and goals_for_current_club > 0
RETURN p.player_id AS Player_ID, 
       p.name AS Player_Name,
       p.current_club_name AS Latest_Club,
       goals_for_current_club as Goals_For_Latest_Club,
       Goals_Scored as Goals_Scored,
       round(goals_for_current_club *1.0 / Goals_Scored, 2) AS Goal_Ratio
ORDER BY Goal_Ratio DESC, Goals_For_Latest_Club DESC
LIMIT(1000)
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
RETURN valuationMonth as Valudation_Date, totalValuation as Total_Valuation_Across_The_Globe
ORDER BY Valudation_Date
"""


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""
This query calculates the total valuation of all players in the entire dataset in a yearly basis.
Returns the year and total valuation in that year.

Return format:
[
    {
        "Year": 2005,
        "Total_Valuation_Across_The_Globe": 10000000000
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
RETURN year as Year, totalValuation as Total_Valuation_Across_The_Globe
ORDER BY Year
"""


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

"""
This query calculates the total number of games played per season per club.
Returns the season, club name and number of games played.

Return format:
[
    {
        "Season": 2005,
        "Matches_Played": 50,
        "Number_of_Distinct_Competitions": 3
    }
]
"""

GAMES_PER_SEASON_PER_CLUB = """
MATCH (c:Club {name: 'Liverpool Football Club'}) 
MATCH (g:Game)
WHERE g.home_club_id = c.club_id OR g.away_club_id = c.club_id
WITH g.season AS season, COUNT(g) AS numberOfGames, COLLECT(DISTINCT g.competition_id) AS competitions
RETURN season as Season, 
       numberOfGames as Matches_Played, 
       SIZE(competitions) AS Number_of_Distinct_Competitions
ORDER BY Season
"""

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------









