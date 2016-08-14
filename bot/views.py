import json
import re
from pprint import pprint

from django.conf import settings
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from bot.connectors import FBConnector
from bot.processors import FBProcessor
from game.utils import Coordinate


def process_facebook_postback(fb_id, postback):
    fb_processor = FBProcessor(fb_id)
    payload = postback.get("payload")

    if not payload:
        return
    else:
        payload = json.loads(payload)
    action = payload.get("action")

    fb_processor.process_action(action)


def process_facebook_message(fb_id, received_msg):
    fb_processor = FBProcessor(fb_id)

    if "quick_reply" in received_msg:
        payload = received_msg.get("quick_reply", {}).get("payload")
        if not payload:
            return
        else:
            payload = json.loads(payload)
        action = payload.get("action")

        fb_processor.process_action(action)

    else:
        match = re.search(r"\(\s*\d\d?\s*,\s*\d\d?\s*\)", received_msg.get("text"))
        if match:
            coordinate = Coordinate.str_to_coordinate(match.group(0))
            fb_processor.process_player_move(coordinate)
        else:
            fb_processor.ask_to_play()


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
                elif "postback" in message:
                    if getattr(settings, "DEBUG", None):
                        pprint(message)
                    process_facebook_postback(message['sender']['id'], message['postback'])
        return HttpResponse()