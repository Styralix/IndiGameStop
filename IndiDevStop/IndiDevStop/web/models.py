from django.contrib.auth import get_user_model
from django.db import models

from IndiDevStop.accounts.models import Profile


UserModel = get_user_model()


class Game(models.Model):
    INDIE = "Indie"
    ACTION = "Action"
    ADVENTURE = "Adventure"
    CASUAL = "Casual"
    RPG = "Rpg"
    COMPLICATED = "Complicated"

    TYPES = [(x, x) for x in (INDIE, ACTION, ADVENTURE, CASUAL, RPG, COMPLICATED)]
    NAME_MAX_LENGTH = 30

    title = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    picture = models.ImageField(
        null=False,
        blank=False,
        validators=(

        )
    )

    likes = models.ManyToManyField(
        UserModel,
        related_name='blog_game',
    )

    description = models.TextField(
        null=False,
        blank=False,
        max_length=70,
    )

    type = models.CharField(
        max_length=max(len(x) for (x, _) in TYPES),
        choices=TYPES,
    )

    release_date = models.DateField(
        null=True,
        blank=True,
    )

    download_link = models.URLField()

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Post(models.Model):
    NAME_MAX_LENGTH = 30

    title = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    body = models.TextField(
        max_length=255,
    )

    date_added = models.DateField(
        auto_now_add=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Game, on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE,
    )

    content = models.TextField(
        max_length=80,

    )

    date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username
