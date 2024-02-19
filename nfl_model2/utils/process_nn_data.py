"""
This script creates and populates the MLData table in the database.

The data from the MLData table is used for training and testing the 
neural network used for improving the Elo model spread predictions.
"""

from ..models import Team, Game, NNData, connect_to_database

connect_to_database()


# check that there are no nndata objects already in the database
if NNData.objects.first() is not None:
    print("There are already nndata objects in the database. Exiting now.")
    exit()

team_names = Team.objects.only("name")

# build first year lists for every field
last_14_games = {}
for team in team_names:
    print(f"processing: {team.name}")
    last_14_games[team.name] = {
        "pregame_elo_for": [],
        "pregame_elo_against": [],
        "points_for": [],
        "points_against": [],
        "yards_for": [],
        "yards_against": [],
        "turnovers_for": [],
        "turnovers_against": [],
    }

first_year_games = Game.objects(season="2010-2011").order_by("id").select_related(2)

def add_game_data(game, last_14_games):
    home_team = game.home_team.name
    away_team = game.away_team.name

    last_14_games[home_team]["pregame_elo_for"].append(game.home_pregame_elo)
    last_14_games[home_team]["pregame_elo_against"].append(game.away_pregame_elo)
    last_14_games[home_team]["points_for"].append(game.home_points)
    last_14_games[home_team]["points_against"].append(game.away_points)
    last_14_games[home_team]["yards_for"].append(game.home_yards)
    last_14_games[home_team]["yards_against"].append(game.away_yards)
    last_14_games[home_team]["turnovers_for"].append(game.away_turnovers)
    last_14_games[home_team]["turnovers_against"].append(game.home_turnovers)

    last_14_games[away_team]["pregame_elo_for"].append(game.away_pregame_elo)
    last_14_games[away_team]["pregame_elo_against"].append(game.home_pregame_elo)
    last_14_games[away_team]["points_for"].append(game.away_points)
    last_14_games[away_team]["points_against"].append(game.home_points)
    last_14_games[away_team]["yards_for"].append(game.away_yards)
    last_14_games[away_team]["yards_against"].append(game.home_yards)
    last_14_games[away_team]["turnovers_for"].append(game.home_turnovers)
    last_14_games[away_team]["turnovers_against"].append(game.away_turnovers)

def pop_game_data(game, last_14_games):
    home_team = game.home_team.name
    away_team = game.away_team.name

    last_14_games[home_team]["pregame_elo_for"].pop(0)
    last_14_games[home_team]["pregame_elo_against"].pop(0)
    last_14_games[home_team]["points_for"].pop(0)
    last_14_games[home_team]["points_against"].pop(0)
    last_14_games[home_team]["yards_for"].pop(0)
    last_14_games[home_team]["yards_against"].pop(0)
    last_14_games[home_team]["turnovers_for"].pop(0)
    last_14_games[home_team]["turnovers_against"].pop(0)
    last_14_games[away_team]["pregame_elo_for"].pop(0)
    last_14_games[away_team]["pregame_elo_against"].pop(0)
    last_14_games[away_team]["points_for"].pop(0)
    last_14_games[away_team]["points_against"].pop(0)
    last_14_games[away_team]["yards_for"].pop(0)
    last_14_games[away_team]["yards_against"].pop(0)
    last_14_games[away_team]["turnovers_for"].pop(0)
    last_14_games[away_team]["turnovers_against"].pop(0)

print("processing first year games.")
for game in first_year_games:
    
    add_game_data(game, last_14_games)

    if len(game.week) > 3 or int(game.week) > 14:
        pop_game_data(game, last_14_games)

rest_of_games = Game.objects(season__ne="2010-2011").order_by("id").select_related(2)

nndata_objects = []
print("processing rest of the games.")
for game in rest_of_games:
    if len(game.week) > 2:
        week += 1
    else: 
        week = int(game.week)

    home_team = game.home_team.name
    away_team = game.away_team.name

    # make nndata object
    nndata = NNData(week_number=week)
    nndata.home_pregame_elo = game.home_pregame_elo
    nndata.away_pregame_elo = game.away_pregame_elo
    nndata.home_pregame_elo_for = last_14_games[home_team]["pregame_elo_for"]
    nndata.home_pregame_elo_against = last_14_games[home_team]["pregame_elo_against"]
    nndata.home_points_for = last_14_games[home_team]["points_for"]
    nndata.home_points_against = last_14_games[home_team]["points_against"]
    nndata.home_yards_for = last_14_games[home_team]["yards_for"]
    nndata.home_yards_against = last_14_games[home_team]["yards_against"]
    nndata.home_turnovers_for = last_14_games[home_team]["turnovers_for"]
    nndata.home_turnovers_against = last_14_games[home_team]["turnovers_against"]
    nndata.away_pregame_elo_for = last_14_games[away_team]["pregame_elo_for"]
    nndata.away_pregame_elo_against = last_14_games[away_team]["pregame_elo_against"]
    nndata.away_points_for = last_14_games[away_team]["points_for"]
    nndata.away_points_against = last_14_games[away_team]["points_against"]
    nndata.away_yards_for = last_14_games[away_team]["yards_for"]
    nndata.away_yards_against = last_14_games[away_team]["yards_against"]
    nndata.away_turnovers_for = last_14_games[away_team]["turnovers_for"]
    nndata.away_turnovers_against = last_14_games[away_team]["turnovers_against"]

    nndata_objects.append(nndata)

    add_game_data(game, last_14_games)
    pop_game_data(game, last_14_games)

# write nndata objects to db
print("writing objects to db.")
NNData.objects.insert(nndata_objects)