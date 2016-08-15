import json

from bot.connectors import FBConnector
from bot.models import FBUser
from bot.utils import Enum
from game.models import Battle

ACTIONS = Enum(["PLAY_GAME",
                "DO_NOT_PLAY_GAME",
                "CONTINUE_GAME",
                "FINISH_GAME",
                "HIT",
                "MISS"
                ])


class FBProcessor:
    def __init__(self, fb_id):
        self.fb_id = fb_id
        fb_user, created = FBUser.objects.get_or_create(fb_id=fb_id)
        self.fb_user = fb_user
        if created:
            user_details = FBConnector.get_user_details(fb_id)
            fb_user.first_name = user_details.get('first_name')
            last_name = user_details.get('last_name')
            if last_name:
                fb_user.last_name = last_name
            fb_user.save()
            FBConnector.post_message(fb_id, "Hi " + fb_user.first_name)

    @staticmethod
    def create_payload(action, **kwargs):
        p = dict()
        if action in ACTIONS:
            p["action"] = action
        else:
            raise ValueError("Wrong action")
        if kwargs:
            p.update(kwargs)

        return json.dumps(p)

    def process_action(self, action):
        process = {
            ACTIONS.PLAY_GAME: self.play_game,
            ACTIONS.DO_NOT_PLAY_GAME: self.do_not_play_game,
            ACTIONS.CONTINUE_GAME: self.continue_game,
            ACTIONS.FINISH_GAME: self.finish_game,
            ACTIONS.HIT: self.process_hit,
            ACTIONS.MISS: self.process_miss
            }.get(action)

        if process:
            process()

    def play_game(self):
        self.battle, created = Battle.objects.get_or_create(player=self.fb_user, status=Battle.ACTIVE)
        if not created:
            FBConnector.post_quick_replies(self.fb_id, "You have unfinished battle. "
                                                  "Do you want to continue or finish it?", [
            FBConnector.create_quick_reply("Continue",
                                           FBProcessor.create_payload(ACTIONS.CONTINUE_GAME)),
            FBConnector.create_quick_reply("Finish",
                                           FBProcessor.create_payload(ACTIONS.FINISH_GAME))
                                           ])
        else:
            FBConnector.post_message(self.fb_id, "Ok, let's start. Please enter coordinates (ex. (1, 4))")

    def continue_game(self):
        FBConnector.post_message(self.fb_id, "Ok, let's continue. Please enter coordinates (ex. (1, 4))")

    def finish_game(self):
        try:
            battle = Battle.objects.get(player=self.fb_user, status=Battle.ACTIVE)
        except Battle.DoesNotExist:
            return
        battle.status = Battle.FINISHED
        battle.save()
        FBConnector.post_quick_replies(self.fb_id, "You previous battle is finished. "
                                              "Would you like to start new battle?", [
           FBConnector.create_quick_reply("Yes",
                                          FBProcessor.create_payload(ACTIONS.PLAY_GAME)),
           FBConnector.create_quick_reply("No",
                                          FBProcessor.create_payload(ACTIONS.DO_NOT_PLAY_GAME))
                                       ])

    def do_not_play_game(self):
        FBConnector.post_message(self.fb_id, "Ok, maybe next time.")

    def process_hit(self):
        try:
            battle = Battle.objects.get(player=self.fb_user, status=Battle.ACTIVE)
        except Battle.DoesNotExist:
            return
        battle.process_player_reply(Battle.HIT)
        if battle.computer_has_won():
            battle.status = Battle.FINISHED
            battle.save()
            FBConnector.post_quick_replies(self.fb_id, "I won. Would you like to start new battle?", [
                FBConnector.create_quick_reply("Yes",
                                               FBProcessor.create_payload(ACTIONS.PLAY_GAME)),
                FBConnector.create_quick_reply("No",
                                               FBProcessor.create_payload(ACTIONS.DO_NOT_PLAY_GAME))
            ])
        else:
            FBConnector.post_message(self.fb_id, "Ok, let's continue. Please enter coordinates (ex. (1, 4))")

    def process_miss(self):
        try:
            battle = Battle.objects.get(player=self.fb_user, status=Battle.ACTIVE)
        except Battle.DoesNotExist:
            return
        battle.process_player_reply(Battle.MISS)
        FBConnector.post_message(self.fb_id, "Ok, let's continue. Please enter coordinates (ex. (1, 4))")

    def process_player_move(self, coordinate):
        try:
            battle = Battle.objects.get(player=self.fb_user, status=Battle.ACTIVE)
        except Battle.DoesNotExist:
            return
        result = battle.make_player_move(coordinate)
        if result[0] == Battle.SHIP_DESTROYED:
            text = "Congratulation, you've destroyed my {}.".format(result[1])
        elif result[0] == Battle.MISS:
            text = "You've missed."
        else:
            text = "You've hit."
        if battle.player_has_won():
            battle.status = Battle.FINISHED
            battle.save()
            FBConnector.post_quick_replies(self.fb_id, "You won. Would you like to start new battle?", [
                FBConnector.create_quick_reply("Yes",
                                               FBProcessor.create_payload(ACTIONS.PLAY_GAME)),
                FBConnector.create_quick_reply("No",
                                               FBProcessor.create_payload(ACTIONS.DO_NOT_PLAY_GAME))
            ])
        else:
            guess = battle.make_guess()
            text = "{} \n My guess is {} . Did I hit or miss?".format(text, guess)
            FBConnector.post_quick_replies(self.fb_id, text, [
                FBConnector.create_quick_reply("Hit",
                                               FBProcessor.create_payload(ACTIONS.HIT)),
                FBConnector.create_quick_reply("Miss",
                                               FBProcessor.create_payload(ACTIONS.MISS))
            ])

    def ask_to_play(self):
        FBConnector.post_quick_replies(self.fb_id, "Would you like to play battleship?", [
            FBConnector.create_quick_reply("Yes", FBProcessor.create_payload(ACTIONS.PLAY_GAME)),
            FBConnector.create_quick_reply("No", FBProcessor.create_payload(ACTIONS.DO_NOT_PLAY_GAME))
        ])