from mongoengine import Document, connect
from mongoengine.queryset import queryset_manager
from mongoengine.fields import StringField, FloatField, IntField, ReferenceField, BooleanField

def connect_to_database(db_name="nfl_model"):
    username = input("Enter DB username: ")
    password = input("Enter DB password: ")
    connect(db="nfl_model", username=username, password=password,
                        host=f"mongodb+srv://{username}:{password}@cluster0.yi9feah.mongodb.net/{db_name}?retryWrites=true&w=majority")
    print("Successfully connected to database.")

class Team(Document):
    name = StringField(required=True, max_length=100)
    ticker = StringField(required=True, max_length=4)
    latitude = FloatField()
    longitude = FloatField()
    elo = IntField()


class Game(Document):
    season = StringField(required=True, max_length=9)
    week = StringField(required=True)
    day = StringField(max_length=3)
    home_team = ReferenceField(Team)
    away_team = ReferenceField(Team)
    home_points = IntField()
    away_points = IntField()
    home_yards = IntField()
    away_yards = IntField()
    home_turnovers = IntField()
    away_turnovers = IntField()
    home_pregame_elo = IntField()
    away_pregame_elo = IntField()
    home_bye = BooleanField()
    away_bye = BooleanField()
    neutral_destination = ReferenceField(Team)