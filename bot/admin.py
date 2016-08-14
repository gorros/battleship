from django.contrib import admin
from .models import FBUser


class FBUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'fb_id', 'created')
    search_fields = ["first_name"]
    ordering = ["created"]

admin.site.register(FBUser, FBUserAdmin)


