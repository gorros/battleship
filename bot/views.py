import json
from pprint import pprint

from django.conf import settings
from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.
from bot.connectors import FBConnector
from bot.models import FBUser
from bot.utils import Enum

ACTIONS = Enum(["PLAY_GAME", "DO_NOT_PLAY_GAME"])


def create_payload(action, **kwargs):
    p = dict()
    if action in ACTIONS:
        p["action"] = action
    else:
        raise ValueError("Wrong action")
    if kwargs:
        p.update(kwargs)

    return json.dumps(p)


def process_facebook_message(fb_id, received_msg):
    fb_user, created = FBUser.objects.get_or_create(fb_id=fb_id)
    if created:
        user_details = FBConnector.get_user_details(fb_id)
        fb_user.first_name = user_details.get('first_name')
        last_name = user_details.get('last_name')
        if last_name:
            fb_user.last_name = last_name
        fb_user.save()
        FBConnector.post_message(fb_id, "Hi " + fb_user.first_name)

    if "quick_reply" in received_msg:
        payload = received_msg.get("quick_reply", {}).get("payload")
        if not payload:
            return
        else:
            payload = json.loads(payload)
        action = payload.get("action")
        if action not in ACTIONS:
            return

        elif action == ACTIONS.PLAY_GAME:
            FBConnector.post_message(fb_id, "Ok, let's start.")

        elif action == ACTIONS.DO_NOT_PLAY_GAME:
            FBConnector.post_message(fb_id, "Ok, maybe next time.")

    else:
        create_quick_replies = [
            FBConnector.create_quick_reply("Yes", create_payload(ACTIONS.PLAY_GAME)),
            FBConnector.create_quick_reply("No", create_payload(ACTIONS.DO_NOT_PLAY_GAME))
        ]
        FBConnector.post_quick_replies(fb_id, "Would you like to play battleship?", create_quick_replies)


class FBBotView(generic.View):
    def get(self, request):
        if request.GET.get("hub.mode") == "subscribe" and request.GET.get('hub.challenge'):
            if request.GET.get("hub.verify_token") == FBConnector.VERIFY_TOKEN:
                return HttpResponse(request.GET['hub.challenge'])
            else:
                return HttpResponse('Error, invalid token')
        else:
            return HttpResponse('')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    if getattr(settings, "DEBUG", None):
                        pprint(message)
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    process_facebook_message(message['sender']['id'], message['message'])
        return HttpResponse()