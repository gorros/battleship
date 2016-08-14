import random

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from django.db.models import Sum
from jsonfield import JSONField

from game import app_settings
from game.utils import Coordinate


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

    HIT = 1
    MISS = 0
    SHIP_DESTROYED = 2

    player = models.ForeignKey(app_settings.PLAYER_MODEL)
    player_board = JSONField(default={str(Coordinate(x, y)): -1 for x in range(1, 11) for y in range(1, 11)})
    computer_board = JSONField(default={str(Coordinate(x, y)): 0 for x in range(1, 11) for y in range(1, 11)})
    turn = models.IntegerField(choices=TURN_CHOICES, default=PLAYER)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)

    def set_up_computer_board(self):
        for category in Ship.CATEGORY_CHOICES:
            ship = Ship(battle=self, category=category[0], health=category[0])
            ship.place_on_board()
            ship.save()

    def make_player_move(self, coordinate):
        Move.objects.create(battle=self, by=Move.PLAYER, x=coordinate.x, y=coordinate.y)
        coord_str = str(coordinate)
        result = self.computer_board.get(coord_str)
        if result != 0:
            ship = self.ships.get(id=result)
            ship.coordinates[coord_str] = Ship.DAMAGED
            ship.health -= 1
            ship.save()
            if ship.health == 0:
                return Battle.SHIP_DESTROYED, ship.get_category_display()
            else:
                return Battle.HIT, "Hit"
        else:
            return Battle.MISS, "Miss"

    def make_guess(self):
        # TODO: Make algorithm smarter
        while True:
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            coord_str = str(Coordinate(x, y))
            if self.player_board.get(coord_str) == -1:
                Move.objects.create(battle=self, by=Move.COMPUTER, x=x, y=y)
                break

        return coord_str  # Should return str or Coordinate?

    def process_player_reply(self, reply):
        if reply == Battle.HIT:
            move = self.moves.filter(by=Move.COMPUTER).order_by('-created')[0]
            self.player_board[str(Coordinate(move.x, move.y))] = Battle.HIT
            # TODO: consider creating user ships
        elif reply == Battle.MISS:
            move = self.moves.filter(by=Move.COMPUTER).order_by('-created')[0]
            self.player_board[str(Coordinate(move.x, move.y))] = Battle.MISS
        self.save()

    def get_computer_total_health(self):
        return self.ships.aggregate(Sum('health')).get('health__sum')

    def computer_has_won(self):
        computer_hit_count = sum(x for x in self.player_board.values() if x == 1)
        if computer_hit_count >= Ship.get_total_initial_health():
            return True
        else:
            return False

    def player_has_won(self):
        return self.get_computer_total_health() == 0


class Ship(TimeStampedModel):
    AIRCRAFT_CONTAINER = 5
    BATTLE_SHIP = 4
    CRUISER = 3
    DESTROYER = 2
    SUBMARINE = 1

    DAMAGED = 1
    INTACT = 0

    CATEGORY_CHOICES = (
        (AIRCRAFT_CONTAINER, 'Aircraft container'),
        (BATTLE_SHIP, 'Battle ship'),
        (CRUISER, 'Cruiser'),
        (DESTROYER, 'Destroyer'),
        (SUBMARINE, 'Submarine'),
    )

    battle = models.ForeignKey(Battle, related_name='ships')
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    health = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
    coordinates = JSONField()

    def place_on_board(self):
        while True:
            self.coordinates = dict()
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            o = random.choice(['v', 'h'])
            for i in range(self.category):
                coord_str = str(Coordinate(x + i, y)) if o == 'v' else str(Coordinate(x, y + i))
                if self.battle.computer_board.get(coord_str) != 0:
                    break
                else:
                    self.coordinates.update({coord_str: Ship.INTACT})
            else:
                break
            continue

        self.save()
        for coord in self.coordinates.keys():
            self.battle.computer_board[coord] = self.id

    @classmethod
    def get_total_initial_health(cls):
        return sum(choice[0] for choice in cls.CATEGORY_CHOICES)


class Move(TimeStampedModel):
    COMPUTER = 0
    PLAYER = 1
    MOVE_BY_CHOICES = (
        (COMPUTER, 'Computer'),
        (PLAYER, 'Player')
    )

    battle = models.ForeignKey(Battle, related_name='moves')
    by = models.IntegerField(choices=MOVE_BY_CHOICES)
    x = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    y = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
