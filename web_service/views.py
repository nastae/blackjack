from .models import Game, Card
import modules.generate_card as generate
import modules.response_utils as response
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def card(request):
    if request.method == "POST":
        card = Card(game=Game.objects.get(id=request.POST.get('gameId')),
                    to_dealer=request.POST.get('toDealer'),
                    type=generate.type(),
                    value=generate.value())
        print('Before save')
        print(card)
        card.save()
        print('After save')
        print(card)
        return response.card_response(card)
    else:
        return response.error_response()


@csrf_exempt
def game(request):
    if request.method == "PUT":
        params = request.PUT
        game = Game.objects.filter(id=params.get('id')).first()
        if params.get('status') is not None:
            game.status = params.get('status')
        if params.get('bet') is not None:
            game.bet = params.get('bet')
        game.save()
        return response.game_response(game)
    elif request.method == "POST":
        params = request.POST
        game = Game(player=params.get('player'),
                    bet=params.get('bet'))
        game.save()
        return response.game_response(game)
    else:
        return response.error_response()


@csrf_exempt
def total(request):
    if request.method == "GET":
        cards = Card.objects.filter(game=request.GET.get('gameId'),
                                    to_dealer=request.GET.get('toDealer'))
        return response.total_response(cards)
    else:
        return response.error_response()
