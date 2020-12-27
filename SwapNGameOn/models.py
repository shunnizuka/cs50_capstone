from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    requestTitle1 = models.CharField(max_length=255)
    requestTitle2 = models.CharField(max_length=255)
    requestTitle3 = models.CharField(max_length=255)
    meetupArea = models.CharField(max_length=255)

class Game(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="games_listed")
    title = models.CharField(max_length=255)

class Swap(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="swap_game")
    startDate = models.DateField()
    endDate = models.DateField()
    hasRequestedGame = models.BooleanField(default=False)
    meetup = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=255)

class Rating(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_rating")
    rating = models.IntegerField()