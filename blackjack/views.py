from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request):
    return render(request, "index.html")


@csrf_exempt
def game(request):
    name = request.POST.get("name")
    context = {
        'player': {
            'name': name,
            'fund': '100'
        }
    }
    return render(request, "game.html", context)
