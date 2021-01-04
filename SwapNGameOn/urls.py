from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("logOut", views.logout_view, name="logOut"),
    path("profile/<int:user>", views.profile, name="profile"),
    path("requests/<int:user>", views.requests, name="requests"),
    path("swaps", views.swaps, name="swaps"),
    path("addGame/<int:user>", views.addGame, name="addGame"),
    path("newRequest/<int:gameId>", views.makeRequest, name="newRequest"),
    
    # post request paths
    path("editProfile/<int:user>", views.editProfile, name="editProfile"),
    path("deleteGame", views.deleteGame, name="deleteGame"),
    path("addRating", views.addRating, name="addRating"),
    path("declineRequest", views.declineRequest, name="declineRequest"),
    path("acceptRequest", views.acceptRequest, name="acceptRequest"),
    path("cancelRequest", views.cancelRequest, name="cancelRequest")
]