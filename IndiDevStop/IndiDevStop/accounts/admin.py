from django.contrib import admin

from django.contrib.auth import get_user_model


from IndiDevStop.accounts.models import Profile, IndiGameUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(IndiGameUser)
class ProfileUserAdmin(admin.ModelAdmin):
    pass
