from django.urls import path
from web_service import views


urlpatterns = [
    path('game', views.game, name='game'),
    path('card', views.card, name='card'),
    path('total', views.total, name='total')
]
