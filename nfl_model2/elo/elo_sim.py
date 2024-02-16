"""
This script simulates previous seasons by calculating the Elo score for every game
that has been played since 2010 and stores the resulting pregame elo 
prediction in the Games collection in the database.
"""


from mongoengine import connect
from ..models import Team, Game, connect_to_database
from .elo_model import post_game_elo_shift, pre_season_elo, pregame_elo_shift
from pymongo import UpdateOne

def run():
    check = input("WARNING this script modifies the database.\nDo you still wish to continue? [y/n] ")
    
    if check.lower() != "y":
        exit()

    connect_to_database()

    Team.objects.update(set__elo=1505)
    games = Game.objects.order_by("id")

    prev_week = "1"
    prev_season = "2010-2011"
    team_updates = []
    game_updates = []
    for game in games:

        if prev_week != game.week:
            print("week ", prev_week, " simulated")
            Team.objects._collection.bulk_write(team_updates)
            team_updates.clear()
            prev_week = game.week

        if prev_season != game.season:
            # we can ignore the first season because elo is already set 
            # to 1505 for all teams
            for team in Team.objects:
                team.elo = pre_season_elo(team.elo)
                team_updates.append(UpdateOne({"_id": team.id}, {"$set": {"elo": team.elo}}))
            Team.objects._collection.bulk_write(team_updates)
            Game.objects._collection.bulk_write(game_updates)
            team_updates.clear()
            game_updates.clear()

            print("Season ", prev_season, " processed")
            prev_season = game.season

        pre_elo_shift = pregame_elo_shift(game)

        home_team = game.home_team
        away_team = game.away_team

        game.home_pregame_elo = home_team.elo + pre_elo_shift
        game.away_pregame_elo = away_team.elo - pre_elo_shift

        post_elo_shift = post_game_elo_shift(game)
        home_team.elo = game.home_pregame_elo + post_elo_shift
        away_team.elo = game.away_pregame_elo - post_elo_shift
    
        team_updates.append(UpdateOne({"_id": home_team.id}, {"$set": {"elo": home_team.elo}}))
        team_updates.append(UpdateOne({"_id": away_team.id}, {"$set": {"elo": away_team.elo}}))
        game_updates.append(UpdateOne({"_id": game.id}, {"$set": {"home_pregame_elo": game.home_pregame_elo, "away_pregame_elo": game.away_pregame_elo}}))

    Game.objects._collection.bulk_write(game_updates)
            
if __name__ == "__main__":
    run()