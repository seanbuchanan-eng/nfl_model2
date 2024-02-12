"""
This table initializes the database with data from seasons 2010 to 2022.

The resulting database contains the core elements of the website data with
Seasons, Teams, Games, and Weeks, tables. 
"""

import os
import mongoengine

from ..models import Team, Game

teams = {
    "Kansas City Chiefs": [39.099789, -94.578560, "KC"],
    "Houston Texans": [29.760427, -95.369804, "HOU"],
    "Seattle Seahawks": [47.603230, -122.330276, "SEA"],
    "Atlanta Falcons": [33.748997, -84.387985, "ATL"],
    "Buffalo Bills": [42.887691, -78.879372, "BUF"],
    "New York Jets": [40.814947462026176, -74.07665577312015, "NYJ"],
    "Las Vegas Raiders": [36.13138384905654, -115.13169451756163, "LV"],
    "Carolina Panthers": [35.25251233973856, -80.84120226587098, "CAR"],
    "Chicago Bears": [41.84754487986402, -87.67153913855199, "CHI"],
    "Detroit Lions": [42.36480313066512, -83.08960351424362, "DET"],
    "Baltimore Ravens": [39.308003294731584, -76.6205088127477, "BAL"],
    "Cleveland Browns": [41.46606790678101, -81.67222601665915, "CLE"],
    "Jacksonville Jaguars": [30.373130908558224, -81.68590701566833, "JAC"],
    "Indianapolis Colts": [39.82165042217416, -86.14927731202125, "IND"],
    "Green Bay Packers": [44.52030015455375, -88.02808200465094, "GB"],
    "Minnesota Vikings": [44.95461717252483, -93.16928759979443, "MIN"],
    "New England Patriots": [42.09250215474584, -71.2639840458412, "NE"],
    "Miami Dolphins": [25.958159412628838, -80.23881748795804, "MIA"],
    "Washington Commanders": [38.907843649151665, -76.86454540290117, "WAS"],
    "Philadelphia Eagles": [39.90153409172584, -75.1675215028637, "PHI"],
    "Los Angeles Chargers": [33.95369646674758, -118.33909324725614, "LAC"],
    "Cincinnati Bengals": [39.095483938138024, -84.51594106292978, "CIN"],
    "Arizona Cardinals": [33.52738095014831, -112.26238094759978, "ARI"],
    "San Francisco 49ers": [37.4032482976688, -121.96987092942953, "SF"],
    "New Orleans Saints": [29.95130267822774, -90.08121201668786, "NO"],
    "Tampa Bay Buccaneers": [27.976153335923133, -82.50335586092449, "TB"],
    "Los Angeles Rams": [33.95369646674758, -118.33909324725614, "LAR"],
    "Dallas Cowboys": [32.7480062696302, -97.09303478136525, "DAL"],
    "Pittsburgh Steelers": [40.4470587094102, -80.01595342189762, "PIT"],
    "New York Giants": [40.814947462026176, -74.07665577312015, "NYG"],
    "Tennessee Titans": [36.16623854753519, -86.77101512830522, "TEN"],
    "Denver Broncos": [39.74381523382964, -105.02021669123351, "DEN"],
    "St. Louis Rams": [38.627003, -90.199402, "STL"],
    "San Diego Chargers": [32.71533, -117.15726, "SD"],
    "Oakland Raiders": [37.804363, -122.271111, "OAK"]
}

superbowl_locations = {
    '2011': 'Dallas Cowboys',
    '2012': 'Indianapolis Colts',
    '2013': 'New Orleans Saints',
    '2014': 'New York Giants',
    '2015': 'Arizona Cardinals',
    '2016': 'San Francisco 49ers',
    '2017': 'Houston Texans',
    '2018': 'Minnesota Vikings',
    '2019': 'Atlanta Falcons',
    '2020': 'Miami Dolphins',
    '2021': 'Tampa Bay Buccaneers',
    '2022': 'Los Angeles Rams',
    '2023': 'Arizona Cardinals' ,
    '2024': 'Las Vegas Raiders',
    '2025': 'New Orleans Saints'
}

def create_teams(db_teams: dict[str: Team], elo_mean: int) -> None:
    """
    Inserts teams into the database if they don't already exist
    
    Parameters
    ----------
    db_teams : dict[str: Team]
        Dictionary of team objects with their team name as keys.
    elo_mean : int
        Chosen mean value for elo.
    """

    for name, value in teams.items():
        if name in db_teams.keys():
            print("team exists")
        else:
            if name == 'Oakland Raiders':
                name = 'Las Vegas Raiders'
            elif name == 'San Diego Chargers':
                name = 'Los Angeles Chargers'
            elif name == 'St. Louis Rams':
                name = 'Los Angeles Rams'
            elif 'Washington' in name:
                name = 'Washington Commanders'

            Team(name=name, ticker=value[2], latitude=value[0], longitude=value[1], elo=elo_mean).save()

def create_game(cols: list, season: str, db_teams: dict[str: Team]) -> Game:
    """
    Creates a game object.

    Parameters
    -----------
    cols : list
        List of game data scraped from a data file.
    season : str
        Season that the game is played in ex. 2022-2023
    db_teams : dict[str: Team]
        Dictionary of team objects with their team name as keys.

    Returns
    -------
    Game object    
    """

    game = Game(season=season, week=cols[0])

    day = cols[1]
    date = cols[2]
    winner = cols[4]
    symbol = cols[5]
    loser = cols[6]
    winner_points = cols[8]
    loser_points = cols[9]
    winner_yards = cols[10]
    winner_turnovers = cols[11]
    loser_yards = cols[12]
    loser_turnovers = cols[13]

    if winner == 'Oakland Raiders':
        winner = 'Las Vegas Raiders'
    if loser == 'Oakland Raiders':
        loser = 'Las Vegas Raiders'
    if winner == 'San Diego Chargers':
        winner = 'Los Angeles Chargers'
    if loser == 'San Diego Chargers':
        loser = 'Los Angeles Chargers'
    if winner == 'St. Louis Rams':
        winner = 'Los Angeles Rams'
    if loser == 'St. Louis Rams':
        loser = 'Los Angeles Rams'
    if 'Washington' in winner:
        winner = 'Washington Commanders'
    elif 'Washington' in loser:
        loser = 'Washington Commanders'

    if symbol == "":
        game.home_team = db_teams[winner]
        game.away_team = db_teams[loser]
        game.home_points = winner_points
        game.away_points = loser_points
        game.home_yards = winner_yards
        game.away_yards = loser_yards
        game.home_turnovers = winner_turnovers
        game.away_turnovers = loser_turnovers
        game.home_pregame_elo = 0
        game.away_pregame_elo = 0
        game.home_bye = False
        game.away_bye = False
        game.neutral_destination = None
        game.day = day

    elif symbol == '@':
        game.home_team = db_teams[loser]
        game.away_team = db_teams[winner]
        game.home_points = loser_points
        game.away_points = winner_points
        game.home_yards = loser_yards
        game.away_yards = winner_yards
        game.home_turnovers = loser_turnovers
        game.away_turnovers = winner_turnovers
        game.home_pregame_elo = 0
        game.away_pregame_elo = 0
        game.home_bye = False
        game.away_bye = False
        game.neutral_destination = None
        game.day = day

    elif symbol == 'N':
        # assign winner to hometeam and loser to awayteam
        game.home_team = db_teams[winner]
        game.away_team = db_teams[loser]
        game.home_points = winner_points
        game.away_points = loser_points
        game.home_yards = winner_yards
        game.away_yards = loser_yards
        game.home_turnovers = winner_turnovers
        game.away_turnovers = loser_turnovers
        game.home_pregame_elo = 0
        game.away_pregame_elo = 0
        game.home_bye = False
        game.away_bye = False
        # default neutral game destination to superbowl destination
        game.neutral_destination = db_teams[superbowl_locations[date.split("-")[0]]]
        game.day = day

    return game

def run():
    
    password = input("Enter DB password: ")
    mongoengine.connect(db="nfl_model", username="seanbuchanan55", password=password,
                        host="mongodb+srv://seanbuchanan55:{}@cluster0.yi9feah.mongodb.net/nfl_model?retryWrites=true&w=majority".format(password))
    print("Successfully connected to database.")

    elo_mean = 1505

    # make team documents if they don't exist
    db_teams = {team.name: team for team in Team.objects}
    create_teams(db_teams, elo_mean)

    if Game.objects:
        print("game collection must be dropped before it can be initialized.")
        exit()

    games = []
    cwd = os.getcwd()
    for file in os.listdir(os.path.join(cwd, "nfl_model2", "data")):
        start_year = file.split('_')[1].split('.')[0]
        last_digits = str(int(start_year[-2:])+1)
        season = start_year + '-20' + last_digits

        with open(os.path.join(cwd, "nfl_model2", "data", file), "r") as f:
            for line in f:
                cols = line.split(",")

                if cols[0] == "Week":
                    continue
                if cols[2] == "Playoffs":
                    continue
                
                games.append(create_game(cols=cols, season=season, db_teams=db_teams))

        Game.objects.insert(games)
        games.clear()
        print(f"Season {season} successfully written to db.")




    

if __name__ == "__main__":
    run()