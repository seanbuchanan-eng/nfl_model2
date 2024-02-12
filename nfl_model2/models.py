from mongoengine import Document
from mongoengine.queryset import queryset_manager
from mongoengine.fields import StringField, Decimal128Field, IntField, ReferenceField, BooleanField


class Team(Document):
    name = StringField(required=True, max_length=100)
    ticker = StringField(required=True, max_length=4)
    latitude = Decimal128Field()
    longitude = Decimal128Field()
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