import json
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Q

from .models import User, Game, Swap, Category, Rating, Request

# Create your views here.


def index(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":

        categoryFilter = request.POST["categoryFilter"]
        searchFilter = request.POST["searchFilter"]

        if(searchFilter):
            if(categoryFilter != "all"):
                category = Category.objects.filter(name=categoryFilter)
                games = Game.objects.exclude(user=request.user).filter(title__contains=searchFilter, isAvailable=True, category__in=category).order_by('title')
            else:
                games = Game.objects.exclude(user=request.user).filter(
                    title__contains=searchFilter).filter(isAvailable=True).order_by('title')
        else:
            if(categoryFilter != "all"):
                category = Category.objects.filter(
                    name=categoryFilter)
                print(category)
                games = Game.objects.exclude(user=request.user).filter(
                    isAvailable=True, category__in=category).order_by('title')
            else:
                games = Game.objects.exclude(user=request.user).filter(
                    isAvailable=True).order_by('title')

        categories = Category.objects.all()
        return render(request, "SwapNGameOn/index.html", {
            "games": games,
            "categories": categories,
            "selected": categoryFilter
        })

    else:

        games = Game.objects.exclude(user=request.user).filter(
            isAvailable=True).order_by('title')
        categories = Category.objects.all()

        return render(request, "SwapNGameOn/index.html", {
            "games": games,
            "categories": categories,
            "selected": "all"
        })


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

    if not request.user.is_authenticated:
        return redirect('login')

    profileUser = User.objects.get(pk=user)
    games = Game.objects.filter(user=profileUser).order_by("-isAvailable")
    ratingList = Rating.objects.filter(user=profileUser)
    rating = ratingList.aggregate(Avg('rating'))['rating__avg']

    return render(request, "SwapNGameOn/profile.html", {
        "profileUser": profileUser,
        "games": games,
        "rating": rating if rating == None else round(rating, 2),
        "ratingNum": ratingList.count
    })


def requests(request, user):

    if not request.user.is_authenticated:
        return redirect('login')

    requestsSent = Request.objects.filter(requester=request.user)
    swapRequestsSent = Swap.objects.filter(
        request__in=requestsSent).order_by("startDate")

    userGame = Game.objects.filter(user=request.user)
    requestsReceived = Swap.objects.filter(
        game__in=userGame, request__status="processing").order_by("startDate")

    return render(request, "SwapNGameOn/requests.html", {
        "requestSent": swapRequestsSent,
        "requestsReceived": requestsReceived
    })


@csrf_exempt
def swaps(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':

        data = json.loads(request.body)

        swapId = data.get("swapId", "")
        swap = Swap.objects.get(pk=swapId)

        swap.isCompleted = True
        swap.game.isAvailable = True
        swap.request.offeredGame.isAvailable = True
        swap.game.save()
        swap.request.offeredGame.save()
        swap.save()

        return JsonResponse({"message": "Swap has been marked as completed"}, status=201)

    else:

        swapRequests = Swap.objects.filter(Q(request__requester=request.user) | Q(
            game__user=request.user)).filter(request__status="accepted", isCompleted=False).order_by("endDate")

        return render(request, "SwapNGameOn/swaps.html", {
            "swaps": swapRequests
        })


def addGame(request, user):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":

        gameOwner = User.objects.get(pk=user)

        if request.user != gameOwner:
            return JsonResponse({"error": "You do not have permission"}, status=400)

        title = request.POST["title"]
        imageLink = request.POST["image"]
        categoryName = request.POST["category"]
        category = Category.objects.get(name=categoryName)

        game = Game(user=gameOwner, title=title,
                    category=category, imageLink=imageLink)
        game.save()

        return HttpResponseRedirect(reverse('profile', kwargs={'user': user}))

    else:

        categories = Category.objects.all()

        return render(request, "SwapNGameOn/addGame.html", {
            "categories": categories
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

        ratingScore = data.get("rating", "")
        userId = data.get("user", "")
        user = User.objects.get(pk=userId)

        rating = Rating(user=user, rating=ratingScore)
        rating.save()

        return JsonResponse({"message": "Rating added successfully"}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


def makeRequest(request, gameId):

    if not request.user.is_authenticated:
        return redirect('login')

    game = Game.objects.get(pk=gameId)
    offers = Game.objects.filter(user=request.user, isAvailable=True)

    if request.method == "POST":

        offeredGameId = request.POST['offers']
        offeredGame = Game.objects.get(pk=offeredGameId)
        meetUpValue = request.POST['meetup']
        altMeetup = request.POST['altMeetup']
        startDate = request.POST['startDate']
        startDateObj = datetime.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = request.POST['endDate']
        endDateObj = datetime.datetime.strptime(endDate, '%Y-%m-%d')
        contactNumber = request.POST['contactNumber']

        # form validation
        if meetUpValue == 'False' and altMeetup == '':
            return render(request, "SwapNGameOn/requestForm.html", {
                "game": game,
                "offers": offers,
                "message": "Please suggest an alternative meetup place"
            })

        if startDateObj < datetime.datetime.now() or endDateObj < datetime.datetime.now():
            return render(request, "SwapNGameOn/requestForm.html", {
                "game": game,
                "offers": offers,
                "message": "Please select a future date for start/end date"
            })

        if endDateObj <= startDateObj:
            return render(request, "SwapNGameOn/requestForm.html", {
                "game": game,
                "offers": offers,
                "message": "End date must be later than start date"
            })

        gameToSwap = Game.objects.get(pk=gameId)

        hasRequestedGame = False
        if (offeredGame.title == gameToSwap.user.requestTitle1 or offeredGame.title == gameToSwap.user.requestTitle2 or offeredGame.title == gameToSwap.user.requestTitle3):
            hasRequestedGame = True

        newRequest = Request(requester=request.user, hasRequestedGame=hasRequestedGame,
                             offeredGame=offeredGame, meetup=meetUpValue, altMeetup=altMeetup, contactNumber=contactNumber)
        newRequest.save()

        newSwap = Swap(game=gameToSwap, startDate=startDate,
                       endDate=endDate, request=newRequest)
        newSwap.save()

        return HttpResponseRedirect(reverse('requests', kwargs={'user': request.user.id}))

    else:
        return render(request, "SwapNGameOn/requestForm.html", {
            "game": game,
            "offers": offers
        })


@csrf_exempt
def declineRequest(request):

    if request.method == "POST":

        data = json.loads(request.body)

        requestId = data.get("requestId", "")
        request = Request.objects.get(pk=requestId)

        request.status = "declined"
        request.save()

        return JsonResponse({"message": "Request has been declined"}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


@csrf_exempt
def acceptRequest(request):

    if request.method == "POST":

        data = json.loads(request.body)

        requestId = data.get("requestId", "")
        request = Request.objects.get(pk=requestId)
        swap = Swap.objects.get(request=request)

        request.status = "accepted"
        if request.offeredGame.isAvailable == False or swap.game.isAvailable == False:
            request.delete()
            return JsonResponse({"error": "The game is not available anymore"}, status=400)

        request.offeredGame.isAvailable = False
        request.save()
        request.offeredGame.save()

        swap.game.isAvailable = False
        swap.game.save()

        return JsonResponse({"message": "Request has been Accepted", "contactNumber": request.contactNumber, "requester": request.requester.username}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


@csrf_exempt
def cancelRequest(request):

    if request.method == "POST":

        data = json.loads(request.body)

        requestId = data.get("requestId", "")
        request = Request.objects.get(pk=requestId)

        request.delete()

        return JsonResponse({"message": "Request has been cancelled"}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)
