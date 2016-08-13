from pprint import pprint

from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from game.models import Battle


class BattleTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@test.gmail', password='top_secret')
        Battle.objects.all().delete()

    def test_board_setup(self):

        battle = Battle.objects.create(player=self.user)
        battle.set_up_computer_board()
        for x in range(1, 11):
            for y in range(1, 11):
                print(battle.computer_board.get("({},{})".format(x, y)), end="|")
            print()
