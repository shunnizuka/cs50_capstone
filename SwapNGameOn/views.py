import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

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

    return render(request, "SwapNGameOn/profile.html", {
        "profileUser" : profileUser,
        "games" : games
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