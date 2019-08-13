from django.http import JsonResponse
import modules.card_utils as card_utils


def game_response(game):
    return JsonResponse(data={
        'id': game.id,
        'player': game.player,
        'bet': game.bet,
        'status': game.status
    })


def card_response(card):
    return JsonResponse(data={
        'type': card.type,
        'value': card.value
    })


def total_response(cards):
    return JsonResponse({'total': card_utils.sum_cards(cards)})


def error_response():
    return JsonResponse({'status': 'false', 'message': 'Wrong request!'},
                        status=500)
