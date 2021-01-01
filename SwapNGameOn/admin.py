from django.contrib import admin
from .models import User, Game, Swap, Category, Rating, Request

# Register your models here.
admin.site.register(User)
admin.site.register(Game)
admin.site.register(Swap)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Request)