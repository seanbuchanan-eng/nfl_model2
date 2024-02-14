"""
This module contains all of the functions for implementing the 
Elo Model developed by Jay Boice at FiveThirtyEight.
see https://fivethirtyeight.com/methodology/how-our-nfl-predictions-work/
"""

from ..models import Team, Game

import numpy as np


def get_distance(teamA: Team, teamB: Team) -> float:
    """
    Calculates distance between team home locations using the haversine formula.
    
    Parameters
    ----------
    teamA : Team
        team object from the database.
    teamB : Team
        team object from the database.

    Returns:
    --------
    float
        Distance between teams in miles.
    """

    r = 6378.137 #Radius of earth (Km)
    lat_a = np.radians(teamA.latitude)
    lat_b = np.radians(teamB.latitude)
    long_a = np.radians(teamA.longitude)
    long_b = np.radians(teamB.longitude)

    # Haversine formula see: https://en.wikipedia.org/wiki/Haversine_formula
    distance = 2*r*np.arcsin(np.sqrt(np.sin((lat_b-lat_a)/2)**2 + 
    (1 - np.sin((lat_a-lat_b)/2)**2 - np.sin((lat_a+lat_b)/2)**2)*np.sin((long_b-long_a)/2)**2))

    return distance/1.609 # Miles

def pregame_elo_shift(game: Game) -> int:
    """
    Calculate the pregame elo shift for a given game.

    Parameters
    ----------
    game : Game
        game that the elo is to be calculated for

    Returns
    -------
    int
        Amount of elo that needs to be shifted from the away team to the 
        home team. For example, add elo_shift to the home team and subtract 
        from the away team.
    """
    home_team = game.home_team
    away_team = game.away_team

    elo_shift = 0
    # check if it is superbowl
    if game.neutral_destination != None:
        neutral_dest = game.neutral_destination
        home_travel_dist = get_distance(home_team, neutral_dest)
        away_travel_dist = get_distance(away_team, neutral_dest)
        home_team_shift = round(home_travel_dist*0.004)
        away_team_shift = round(away_travel_dist*0.004)
        elo_shift = (away_team_shift - home_team_shift)
    else:
        # regular season game
        distance = get_distance(home_team, away_team)
        elo_shift += 48/2
        elo_shift += round(distance*0.004/2)

        # check for playoffs and multiply by 1.2 if it is
        try:
            int(game.week)
        except ValueError:
            # Error because week is now something like 'WildCard'
            # therefore it is playoffs
            elo_shift = round(elo_shift * 1.2) 
    
    return elo_shift

def win_prob(elo_diff: int) -> float:
    "Calculates win probability with respect to the home team"
    win_probability = 1/(10**(-elo_diff/400)+1)
    return win_probability

def post_game_elo_shift(game: Game) -> int:
    """
    Calculates the points to be added or subtracted to the home team
    based on the game results. The opposite must be done to the away team
    to keep elo a closed system.

    Parameters
    ----------
    game : Game
        Game to have the elo calculated from.

    Returns
    -------
    int
        The number of Elo points that need to be shifted from the away team 
        to the home team based on the game result. Positive indicates points 
        go to the home team, negative indicates points go to the away team.
    """
    home_points = game.home_points
    away_points = game.away_points

    # recommended K-factor
    K = 20

    elo_diff = game.home_pregame_elo - game.away_pregame_elo

    # forcast delta
    win_probability = win_prob(elo_diff)
    if home_points == away_points:
        forecast_delta = 0.5 - win_probability
    elif home_points > away_points:
        forecast_delta = 1 - win_probability
    else:
        forecast_delta = 0 - win_probability

    # mov multiplier
    point_diff = home_points - away_points
    
    if point_diff == 0:
        # The explanation for accounting for a tie doesn't seem to be on the website
        # anymore but I've decided to keep this value because it makes sense 
        # that a team that is predicted to win ties should lose points.
        mov = 1.525
    else:
        if point_diff < 0:
            elo_diff *= -1
        mov = np.log(abs(point_diff)+1)*(2.2/(elo_diff*0.001+2.2))

    return round(K*forecast_delta*mov)

def pre_season_elo(elo):
    """
    Calculate team's pre-season elo rating. It is essentially
    just a regression to the mean.
    
    Parameters:
    -----------
    elo : int
        Elo of a team at the end of a season.

    Returns:
    --------
    int
        New elo value for the team.
    """
    mean = 1505
    new_elo = elo - (elo - mean)/3
    return round(new_elo)