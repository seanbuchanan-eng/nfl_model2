from unittest import TestCase

from .models import Team, Game
from .elo.elo_model import (get_distance, pregame_elo_shift, 
                            win_prob, post_game_elo_shift,
                            pre_season_elo)



class EloModelTests(TestCase):
    
    def setUp(self):
        self.teamA = Team(
            name="Kansas City Chiefs", 
            ticker="KC", 
            latitude=39.099789,
            longitude=-94.57856,
            elo=1750
        )
        self.teamB = Team(
            name="Seattle Seahawks", 
            ticker="SEA", 
            latitude=47.60323,
            longitude=-122.330276,
            elo=1476
        )
        self.teamC = Team(
            name="Dallas Cowboys", 
            ticker="DAL", 
            latitude=32.7480062696302,
            longitude=-97.09303478136525,
            elo=1476
        )
        self.neutral_game = Game(
            season="2010-2011",
            week="SuperBowl",
            day="Sun",
            home_team=self.teamA,
            away_team=self.teamB,
            home_points=31,
            away_points=25,
            home_yards=338,
            away_yards=387,
            home_turnovers=0,
            away_turnovers=3,
            home_pregame_elo=0,
            away_pregame_elo=0,
            home_bye=False,
            away_bye=False,
            neutral_destination=self.teamC
        )
        self.regular_game = Game(
            season="2010-2011",
            week="1",
            day="Sun",
            home_team=self.teamA,
            away_team=self.teamB,
            home_points=31,
            away_points=25,
            home_yards=338,
            away_yards=387,
            home_turnovers=0,
            away_turnovers=3,
            home_pregame_elo=0,
            away_pregame_elo=0,
            home_bye=False,
            away_bye=False,
            neutral_destination=None
        )
        self.playoff_game = Game(
            season="2010-2011",
            week="WildCard",
            day="Sun",
            home_team=self.teamA,
            away_team=self.teamB,
            home_points=31,
            away_points=25,
            home_yards=338,
            away_yards=387,
            home_turnovers=0,
            away_turnovers=3,
            home_pregame_elo=0,
            away_pregame_elo=0,
            home_bye=False,
            away_bye=False,
            neutral_destination=None
        )

    def test_get_distance(self):
        """
        get_distance(teamA, teamB) returns the distance between two team home cities.
        """
        self.assertEquals(get_distance(self.teamA, self.teamB), 1504.6901578432269)
        
    def test_pregame_elo_shift_neutral_game(self):
        self.assertEquals(pregame_elo_shift(self.neutral_game), 5)

    def test_pregame_elo_shift_regular_game(self):
        self.assertGreaterEqual(pregame_elo_shift(self.regular_game), 0)
        self.assertEquals(pregame_elo_shift(self.regular_game), 27)

    def test_pregame_elo_shift_playoff_game(self):
        self.assertGreaterEqual(pregame_elo_shift(self.playoff_game), 0)
        self.assertEquals(pregame_elo_shift(self.playoff_game), round(27 * 1.2))

    def test_win_prob(self):
        self.assertGreaterEqual(win_prob(0), 0)
        self.assertLessEqual(win_prob(100000000000), 1)
        self.assertEquals(win_prob(7), 0.5100724469274385)

    def test_post_game_elo_shift_neutral_game(self):
        self.assertEquals(post_game_elo_shift(self.neutral_game), 19)

    def test_post_game_elo_shift_regular_game(self):
        self.assertGreaterEqual(post_game_elo_shift(self.regular_game), 0)
        self.assertEquals(post_game_elo_shift(self.regular_game), 19)

    def test_post_game_elo_shift_playoff_game(self):
        self.assertGreaterEqual(post_game_elo_shift(self.playoff_game), 0)
        self.assertEquals(post_game_elo_shift(self.playoff_game), 19)

    def test_pre_season_elo(self):
        self.assertEquals(pre_season_elo(1753), 1670)