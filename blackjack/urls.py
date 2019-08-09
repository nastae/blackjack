from django.urls import path
from blackjack import views

urlpatterns = [
    path("", views.home),
    path("game", views.game)
]
