from django.urls import include, path

urlpatterns = [
    path("", include("blackjack.urls")),
    path("api/", include("web_service.urls"))
]
