from django.conf import settings

PLAYER_MODEL = getattr(settings, 'PLAYER_USER_MODEL', 'auth.User')
