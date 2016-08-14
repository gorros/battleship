from django.contrib import admin

# Register your models here.
from game.models import Battle


class BattleAdmin(admin.ModelAdmin):
    list_display = ('player', 'status', 'created')
    search_fields = ["player"]
    ordering = ["created"]

admin.site.register(Battle, BattleAdmin)