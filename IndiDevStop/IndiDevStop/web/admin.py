from django.contrib import admin

# Register your models here.
from IndiDevStop.web.models import Game, Post, Comment


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
