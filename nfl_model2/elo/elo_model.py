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