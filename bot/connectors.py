import json
from pprint import pprint

import requests
import logging
from django.conf import settings


class FBConnector:
    PAGE_ACCESS_TOKEN = "EAAOMnjfeZBJMBAG6KaZCTnuRtkVLSCBnf5ULuWZBYkmyerT8oTUo8qCVM35xy6pzQSEXnM8osH39usezWyKOsS6p0y7cZAr6ZBZB2ZCP4ZBMVr7yXemupmNP2CftPym8qY6tZBzASadnZB1REj8DvDMLHzd3ezRIDZAekbaZBBGcphwm1wZDZD"
    VERIFY_TOKEN = "gorros_token"
    POST_MESSAGE_URL = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    USER_DETAILS_URL = "https://graph.facebook.com/v2.6/{}"

    @classmethod
    def get_user_details(cls, fb_id):
        user_details_url = cls.USER_DETAILS_URL.format(fb_id)
        user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': cls.PAGE_ACCESS_TOKEN}
        user_details = requests.get(user_details_url, user_details_params).json()
        return user_details

    @classmethod
    def post_message(cls, fb_id, msg):
        data = json.dumps({
                            "recipient": {
                                "id": fb_id
                                },
                            "message": {
                                "text": msg
                                }
                            })
        return cls._post(data)

    @classmethod
    def post_buttons(cls, fb_id, text, buttons):
        data = json.dumps({
                            "recipient": {
                                "id": fb_id
                            },
                            "message": {
                                "attachment": {
                                    "type": "template",
                                    "payload": {
                                        "template_type": "button",
                                        "text": text,
                                        "buttons": buttons
                                    }
                                }
                            }
                        })
        return cls._post(data)


    @classmethod
    def post_elements(cls, fb_id, elements):
        data = json.dumps({
                            "recipient":{
                                "id": fb_id
                            },
                            "message": {
                                "attachment":{
                                    "type": "template",
                                    "payload": {
                                        "template_type": "generic",
                                        "elements": elements
                                    }
                                }
                            }
                        })
        return cls._post(data)

    @classmethod
    def post_quick_replies(cls, fb_id, text, quick_replies):
        data = json.dumps({
                        "recipient": {
                            "id": fb_id
                        },
                        "message": {
                            "text": text,
                            "quick_replies": quick_replies
                        }
                    })
        return cls._post(data)

    @classmethod
    def _post(cls, data):
        if getattr(settings, "DEBUG", None):
            pprint(data)
        response = requests.post(cls.POST_MESSAGE_URL,
                                 headers={"Content-Type": "application/json"},
                                 data=data)
        if getattr(settings, "DEBUG", None):
            pprint(response.json())
        return response.json()

    @staticmethod
    def create_element(title, buttons, subtitle=None, image_url=None):
        element = dict(title=title, buttons=buttons)
        if subtitle:
            element["subtitle"] = subtitle
        if image_url:
            element["image_url"] = image_url
        return element

    @staticmethod
    def create_button(button_type, title, payload=None, url=None):
        if button_type == "postback" and payload:
            return dict(type=button_type, title=title, payload=payload)
        elif button_type == "web_url" and url:
            return dict(type=button_type, title=title, url=url)
        else:
            raise ValueError  # TODO: refactor

    @classmethod
    def create_quick_reply(cls, title, payload):
        return dict(content_type="text", title=title, payload=payload)


