import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg

from .models import User, Game, Swap, Category, Rating

# Create your views here.

def index(request):
    return render(request, "SwapNGameOn/layout.html")

def login_view(request):
    if request.method == "POST":
    
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "SwapNGameOn/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "SwapNGameOn/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))
    
def register(request):
    if request.method == "POST":

        username = request.POST["username"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        print(password)
        print(confirmation)
        if password != confirmation:
            return render(request, "SwapNGameOn/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, username, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "SwapNGameOn/register.html", {
                "message": "username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "SwapNGameOn/register.html")

def profile(request, user):

    profileUser = User.objects.get(pk=user)
    games = Game.objects.filter(user=profileUser)
    ratingList = Rating.objects.filter(user=profileUser)
    rating = ratingList.aggregate(Avg('rating'))['rating__avg']

    return render(request, "SwapNGameOn/profile.html", {
        "profileUser" : profileUser,
        "games" : games,
        "rating" : rating if rating == None else round(rating, 2),
        "ratingNum" : ratingList.count
    })

def addGame(request, user):

    if request.method == "POST":

        gameOwner = User.objects.get(pk=user)
        
        if request.user != gameOwner:
            return JsonResponse({"error": "You do not have permission"}, status=400)

        title = request.POST["title"]
        imageLink = request.POST["image"]
        categoryName = request.POST["category"]
        category = Category.objects.get(name=categoryName)

        game = Game(user=gameOwner, title=title, category=category, imageLink=imageLink)
        game.save()

        return HttpResponseRedirect(reverse('profile', kwargs={'user': user}))
    
    else:

        categories = Category.objects.all()

        return render(request, "SwapNGameOn/addGame.html", {
            "categories" : categories
        })

def editProfile(request, user):

    if request.method == "POST":

        profileUser = User.objects.get(pk=user)

        username = request.POST["username"]
        requestTitle1 = request.POST["requestTitle1"]
        requestTitle2 = request.POST["requestTitle2"]
        requestTitle3 = request.POST["requestTitle3"]
        meetupArea = request.POST["meetupArea"]

        profileUser.username = username
        profileUser.requestTitle1 = requestTitle1
        profileUser.requestTitle2 = requestTitle2
        profileUser.requestTitle3 = requestTitle3
        profileUser.meetupArea = meetupArea
        profileUser.save()

        return HttpResponseRedirect(reverse('profile', kwargs={'user': user}))
    
    else:
        return JsonResponse({"error": "POST request required."}, status=400)

@csrf_exempt
def deleteGame(request):

    if request.method == "POST":

        data = json.loads(request.body)

        gameId = data.get("gameId", "")
        gameToDelete = Game.objects.get(pk=gameId)

        if gameToDelete.user != request.user:
            return JsonResponse({"error": "You do not have permission."}, status=400)
        
        gameToDelete.delete()
        
        return JsonResponse({"message": "Game deleted successfully"}, status=201)
    
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


@csrf_exempt
def addRating(request):

    if request.method == "POST":

        data = json.loads(request.body)

        ratingScore = data.get("rating","")
        userId = data.get("user", "")
        user = User.objects.get(pk=userId)

        rating = Rating(user=user, rating=ratingScore)
        rating.save()

        return JsonResponse({"message": "Rating added successfully"}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)