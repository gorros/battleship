import random

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from bot.models import FBUser
from game.models import Battle, Ship
from game.utils import Coordinate


def print_board(board):
    for x in range(1, 11):
        for y in range(1, 11):
            result = Ship.objects.filter(pk=board.get(str(Coordinate(x, y))))
            print(result[0].category if result else 0, end="|")
        print()


def print_player_board(board):
    for x in range(1, 11):
        for y in range(1, 11):
            print(board.get(str(Coordinate(x, y))), end="|")
        print()


def generate_player_board():
    player_board = {str(Coordinate(x, y)): 0 for x in range(1, 11) for y in range(1, 11)}
    for category, _ in Ship.CATEGORY_CHOICES:
        while True:
            coordinates = list()
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            o = random.choice(['v', 'h'])
            for i in range(category):
                coord_str = str(Coordinate(x + i, y)) if o == 'v' else str(Coordinate(x, y + i))
                if player_board.get(coord_str) != 0:
                    break
                else:
                    coordinates.append(coord_str)
            else:
                break
            continue

        for coord in coordinates:
            player_board[coord] = category

    return player_board


class BattleTestCase(TestCase):
    def setUp(self):
        self.user = FBUser.objects.create(fb_id='1111111', first_name='Test')

    def test_board_setup(self):

        battle = Battle.objects.create(player=self.user)
        battle.set_up_computer_board()
        print_board(battle.computer_board)

    def test_make_player_move(self):
        battle = Battle.objects.create(player=self.user)
        battle.set_up_computer_board()
        print_board(battle.computer_board)
        print(20 * '=')
        print(battle.make_player_move(Coordinate(1,3)))
        print(20 * '=')
        print_board(battle.computer_board)

    def test_make_guess(self):
        battle = Battle.objects.create(player=self.user)
        battle.set_up_computer_board()
        print_player_board(battle.player_board)
        print(battle.make_guess())
        battle.process_player_reply(1)
        print_player_board(battle.player_board)
        print(battle.make_guess())
        battle.process_player_reply(0)
        print_player_board(battle.player_board)

    def test_initial_health(self):
        assert Ship.get_total_initial_health() == 18

    def test_game(self):
        battle = Battle.objects.create(player=self.user)
        battle.set_up_computer_board()
        player_board = generate_player_board()
        print("Player board")
        print_player_board(player_board)
        print(20 * '=')
        print("Computer board")
        print_board(battle.computer_board)
        print(20 * '=')

        while not (battle.player_has_won() or battle.computer_has_won()):
            coords_str = input("Enter coordinates: ")
            coordinate = Coordinate.str_to_coordinate(coords_str)
            result = battle.make_player_move(coordinate)
            print(result)
            print(battle.get_computer_total_health())
            print("Guess " + battle.make_guess())
            reply = int(input("Enter reply (1 for hit and 0 for miss): "))
            battle.process_player_reply(reply)



