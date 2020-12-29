from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("profile/<int:user>", views.profile, name="profile"),
    path("addGame/<int:user>", views.addGame, name="addGame")

]