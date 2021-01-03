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
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, related_name="game_category")
    imageLink = models.CharField(max_length=255, null=True)
    isAvailable = models.BooleanField(default=True)

class Swap(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="swap_game")
    startDate = models.DateField()
    endDate = models.DateField()
    isCompleted = models.BooleanField(default=False)
    request = models.ForeignKey("Request", on_delete=models.CASCADE,null=True, related_name="swap_request")

class Request(models.Model):
    requester = models.ForeignKey("User", on_delete=models.CASCADE, related_name="request_user")
    hasRequestedGame = models.BooleanField(default=False)
    offeredGame = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="request_game")
    meetup = models.BooleanField(default=False)
    altMeetup = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default="processing")
    timestamp = models.DateTimeField(auto_now_add=True)
    contactNumber = models.IntegerField(null=True)

class Category(models.Model):
    name = models.CharField(max_length=255)

class Rating(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_rating")
    rating = models.IntegerField()