import app_for_club_per_league from './query_results/app_for_club_per_league.json';
import goals_against_clubs from './query_results/goals_against_clubs.json';
import appereances_against from './query_results/appereances_against.json';
import average_age_per_competition from './query_results/average_age_per_competition.json';
import player_against_club_wins from './query_results/player_against_club_wins.json';
import most_red_cards_between_clubs from './query_results/most_red_cards_between_clubs.json';
import average_valuation_per_game from './query_results/average_valuation_per_game.json';
import most_booked_clubs_per_ref from './query_results/most_booked_clubs_per_ref.json';
import minutes_per_contribution from './query_results/minutes_per_contribution.json';
import local_hero from './query_results/local_hero.json';
import goals_for_country from './query_results/goals_for_country.json';
import points_per_valuation from './query_results/points_per_valuation.json';
import goals_in_country_per_season from './query_results/goals_in_country_per_season.json';
import heated_stadiums from './query_results/heated_stadiums.json';
import avg_champion_point from './query_results/avg_champion_point.json';
import manager_avg_goal_diff from './query_results/manager_avg_goal_diff.json';
import valuation_per_country from './query_results/valuation_per_country.json';
import our_goalscorer from './query_results/our_goalscorer.json';
import valuation_over_time_yearly from './query_results/valuation_over_time_yearly.json';
import matches_per_season from './query_results/matches_per_season.json';

const details = [
    {
        queryId: 0,
        title: "Appearances in a Competition",
        description: 
        "This query returns the players and their appearances grouped by competition and club. Competition Name is input.\n\n" +
        "If he has played in multiple clubs in the given competition, there will be multiple rows for the player.\n\n" +
        "Returns the Player\_ID, Player\_Name, Club\_Name, Appearances, Goals\_Scored, Assists, Yellow\_Cards, Red\_Cards, Minutes\_Played.\n\n"
        ,
        table: app_for_club_per_league
    },
    {
        queryId: 1,
        title: "Goal and Assist Stats Against a Club",
        description: "This query returns the players and their goals and assists grouped by clubs. If he has played against multiple clubs, there will be multiple rows for the player. Returns the Player\_ID, Player\_Name, Own\_Club\_Name, Against\_Club\_Name, Goals\_Scored, Assists",
        table: goals_against_clubs
    },
    {
        queryId: 2,
        title: "Two Players Against Each Other",
        description: "This query returns the players who played against each other the most. Returns the Player\_1\_ID, Player\_1\_Name, player\_2\_id, Player\_2\_Name, Appereances\_Against",
        table: appereances_against
    },
    {
        queryId: 3,
        title: "Average Age in a League",
        description: "This query returns the leagues and the number of players that have played in the league and the average age of the players in the games played, calculated from the date of the game minus the date of birth of the player. Returns the Competition\_ID, Competition\_Name, Total\_Number\_of\_Players, Average\_Age",
        table: average_age_per_competition
    },
    {
        queryId: 4,
        title: "Player Wins Against a Club",
        description: "This query returns the players that got the most wins against a club. The competition name is given by input. Returns the Player\_ID, Player\_Name, Own\_Club\_Name, Against\_Club\_name, Wins, Losses, Draws",
        table: player_against_club_wins
    },
    {
        queryId: 5,
        title: "The Fixture with the Most Red Cards",
        description: "This query returns the pair clubs that played games with the highest red cards. Find red card from the appearances. Returns the Club\_1\_Name, Club\_2\_Name, Red\_Cards",
        table: most_red_cards_between_clubs
    },
    {
        queryId: 6,
        title: "The Games with the Most Expensive Lineups",
        description: "This query returns the games with most average value of players. Calculates the average value of players in each game. The valuation of players is based on the market value of the player in the game. HAS\_VALUATION relationship with the closest and a past date is the real valuation of the player in the game. Returns the Date, Home\_Club, Away\_Club, Average\_Valuation\_of\_Players.",
        table: average_valuation_per_game
    },
    {
        queryId: 7,
        title: "The Referee-Club Pairs with Most Bookings",
        description: "This query returns the referees with their most booked clubs. If the referee has booked multiple clubs, there will be multiple rows for the referee. Returns the Referee\_Name, Club\_Name, Yellow\_Cards, Red\_Cards",
        table: most_booked_clubs_per_ref
    },
    {
        queryId: 8,
        title: "Goal and Assist Contribution per Minute",
        description: "This query returns the players with the lowest minutes played for a goal/assist, in a competition, per season of course. Only players with more than 450 minutes played are considered. (roughly 5 matches) Returns the Season, Competition\_ID, Player\_Name, Minutes\_Per\_Contibution, Total\_Minutes.",
        table: minutes_per_contribution
    },
    {
        queryId: 9,
        title: "Players Carrying the Clubs",
        description: "This query returns the local heroes. Players that have the highest number of goals / team's goals in competition and season. Returns the Player\_Name, Club\_Name, Competition\_Name, Season, Goals\_Scored\_By\_Player, Total\_Club\_Goals, Goals\_Scored, Ratio",
        table: local_hero
    },
    {
        queryId: 10,
        title: "Given Country's Top Scorer",
        description: "This query returns the players with the most goal+assists for a given country and given age range. Returns the Country\_Name, Player\_Name, Goals\_Scored, Assists, Minutes\_Played",
        table: goals_for_country
    },
    {
        queryId: 11,
        title: "Manager Success with respect to Points Gained and Player Valuations",
        description: "Rate of valuations of players in games to points they get in the game, grouped by each manager. This query calculates the success of the manager. The higher the score, the better the manager. Group by manager name, sum of points from score, sum of valuation at that time. Returns the Manager, Average\_Point, Matches\_Played, Average\_Valuation, Score",
        table: points_per_valuation
    },
    {
        queryId: 12,
        title: "Average Goal per Game in Each Country",
        description: "This query returns the countries with most average goal per matches played year by year. Calculated by (Competition)-[:IN\_COUNTRY]->(Country) relationship. Input is year. Season attribute of Game node is used for year. Game node has home club goals and away club goals attributes. Returns the Country\_Name, Goals\_Scored, Matches\_Played, Average\_Goals",
        table: goals_in_country_per_season
    },
    {
        queryId: 13,
        title: "Stadium Aggressiveness with respect to Attendances and Red Cards",
        description: "This query returns the stadiums according to its heat. Heat is calculated by a Score measure. Retrieved by (p:Player)-[ai:APPEARED\_IN]->(g:Game)-[:PLAYED\_IN]->(s:Stadium) relationship. ai.red\_cards attributes are used for red cards. Input is year. Season attribute of Game node is used for year. Game node has attendance attribute. Returns the Stadium, Club, Total\_Attendance, Matches\_Played, Average\_Attendance, Red\_Cards, Average\_Red\_Cards, Score",
        table: heated_stadiums
    },
    {
        queryId: 14,
        title: "Average Points Gained by Champions in Leagues",
        description: "This query returns the average point needed to be champion in a competition. Returns the Competition, Average\_Championship\_Point",
        table: avg_champion_point
    },
    {
        queryId: 15,
        title: "Average Goal Difference for Each Manager",
        description: "This query returns the average goal difference for each coach. Returns the Manager, Average\_Goal\_Difference, Matches\_Played",
        table: manager_avg_goal_diff
    },
    {
        queryId: 16,
        title: "Average Valuation of Players per Country",
        description: "This query returns the average valuation of players in a given year for each country. Returns the Country\_Name, Average\_Valuation, Number\_of\_Players",
        table: valuation_per_country
    },
    {
        queryId: 17,
        title: "Goal Ratio of Players: Current Team / Total",
        description: "This query returns the players with the highest goal ratio for goals scored for the current club and scored in total. Returns the Player\_ID, Player\_Name, Latest\_Club, Goals\_For\_Latest\_Club, Goals\_Scored, Goal\_Ratio",
        table: our_goalscorer
    },
    {
        queryId: 18,
        title: "Total Valuation of All Players Changes Over Time",
        description: "This query calculates the total valuation of all players in the entire dataset in a yearly basis. Returns the year and total valuation in that year. Using a simple Python script, we plotted a simple graph to see the valuation changes over time. As you can see from the plot below, the valuation of the players across the globe is increasing each and every year except for the COVID-19 era. Even with a simple query and a visualisation, we can see the effects of real world phenomena.",
        table: valuation_over_time_yearly
    },
    {
        queryId: 19,
        title: "Games Played per Season for the Given Club",
        description: "This query calculates the total number of games played per season per club. Returns the season, club name and number of games played.",
        table: matches_per_season
    },

]

export default details;