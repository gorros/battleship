from django.conf.urls import url

from bot.views import FBBotView

urlpatterns = [
    url(r'^fb/?$', FBBotView.as_view(), name="fb-bot"),
]
