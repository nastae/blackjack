from django.db import models
import uuid

# statuses: NEW, IN_GAME, FINISHED


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.CharField(max_length=250)
    bet = models.IntegerField()
    status = models.CharField(max_length=50, default='NEW')


class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    to_dealer = models.BooleanField()
    type = models.CharField(max_length=10)
    value = models.CharField(max_length=2)
