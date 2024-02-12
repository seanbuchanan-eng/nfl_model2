"""
This module contains all of the functions for implementing the 
Elo Model developed by Jay Boice at FiveThirtyEight.
see https://fivethirtyeight.com/methodology/how-our-nfl-predictions-work/
"""

from ..models import Team

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