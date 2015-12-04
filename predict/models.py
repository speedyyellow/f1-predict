from django.db import models
from django.contrib.auth.models import User

# Core data
class Team(models.Model):
    name = models.CharField(max_length=50)
    engine = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Driver(models.Model):
    name = models.CharField(max_length=50)
    number = models.IntegerField()
    def __str__(self):
        return self.name

class Circuit(models.Model):
    country = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class FinishingPosition(models.Model):
    position = models.IntegerField()
    points = models.IntegerField()
    def __str__(self):
        return str(self.position)

# per season data
class Season(models.Model):
    name = models.CharField(max_length=5)
    active = models.BooleanField()
    def __str__(self):
        return self.name

class TeamDriver(models.Model):
    season = models.ForeignKey(Season)
    team = models.ForeignKey(Team)
    driver = models.ForeignKey(Driver)
    def __str__(self):
        return self.driver.name + " (" + self.team.name + ")"

class SeasonRound(models.Model):
    season = models.ForeignKey(Season)
    circuit = models.ForeignKey(Circuit)
    date = models.DateField()
    def __str__(self):
        return self.season.name + " " + self.circuit.name 

# result data
class RaceResult(models.Model):
    season_round = models.ForeignKey(SeasonRound)
    pole_position = models.ForeignKey(TeamDriver, related_name="result_pole_position", null=True)
    fastest_lap = models.ForeignKey(TeamDriver, related_name="result_fastest_lap", null=True)
    def __str__(self):
        return self.season_round.season.name + " " + self.season_round.circuit.country

class ResultPosition(models.Model):
    result = models.ForeignKey(RaceResult)
    position = models.ForeignKey(FinishingPosition)
    driver = models.ForeignKey(TeamDriver)
    def __str__(self):
        return str(self.position.position) + " " + self.driver.driver.name + " " + self.result.season_round.circuit.country

# player data
class Prediction(models.Model):
    created = models.DateTimeField()
    user = models.ForeignKey(User, null=True)
    pole_position = models.ForeignKey(TeamDriver, related_name="prediction_pole_position", null=True)
    fastest_lap = models.ForeignKey(TeamDriver, related_name="prediction_fastest_lap", null=True)
    def __str__(self):
        return self.user.email + " " + str(self.created)

class PredictionPosition(models.Model):
    prediction = models.ForeignKey(Prediction)
    position = models.ForeignKey(FinishingPosition)
    driver = models.ForeignKey(TeamDriver)











