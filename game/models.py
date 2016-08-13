import random

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from jsonfield import JSONField

from game import app_settings


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Battle(TimeStampedModel):
    COMPUTER = 0
    PLAYER = 1
    TURN_CHOICES = (
        (COMPUTER, 'Computer'),
        (PLAYER, 'Player')
    )

    ACTIVE = 0
    FINISHED = 1
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (FINISHED, 'Finished'),
    )

    player = models.ForeignKey(app_settings.PLAYER_MODEL)
    player_board = JSONField(default={})
    computer_board = JSONField(default={"({},{})".format(x, y): 0 for x in range(1, 11) for y in range(1, 11)})
    turn = models.IntegerField(choices=TURN_CHOICES, default=PLAYER)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)

    def set_up_computer_board(self):
        for category in Ship.CATEGORY_CHOICES:
            ship = Ship(battle=self, category=category[0], health=category[0])
            ship.place_on_board()
            ship.save()


class Ship(TimeStampedModel):
    AIRCRAFT_CONTAINER = 5
    BATTLE_SHIP = 4
    CRUISER = 3
    DESTROYER = 2
    SUBMARINE = 1

    CATEGORY_CHOICES = (
        (AIRCRAFT_CONTAINER, 'Aircraft container'),
        (BATTLE_SHIP, 'Battle ship'),
        (CRUISER, 'Cruiser'),
        (DESTROYER, 'Destroyer'),
        (SUBMARINE, 'Submarine'),
    )

    battle = models.ForeignKey(Battle)
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    health = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
    coordinates = JSONField(default=[])

    @property
    def is_destroyed(self):
        return self.health == 0

    def place_on_board(self):
        while True:
            self.coordinates = list()
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            o = random.choice(['v', 'h'])
            for i in range(self.category):
                if o == 'v':
                    coord_str = "({},{})".format(x + i, y)
                else:
                    coord_str = "({},{})".format(x, y + i)
                if self.battle.computer_board.get(coord_str) != 0:
                    break
                else:
                    self.coordinates.append(coord_str)
            else:
                break
            continue

        for coord in self.coordinates:
            self.battle.computer_board[coord] = self.category
