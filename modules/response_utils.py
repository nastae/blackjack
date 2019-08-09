from django.http import JsonResponse


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


def error_response():
    return JsonResponse({'status': 'false', 'message': 'Wrong request!'},
                        status=500)
