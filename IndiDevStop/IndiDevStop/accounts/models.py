from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import models as auth_models

from IndiDevStop.accounts.managers import IndiGameManager
from IndiDevStop.common.validators import validate_only_letters


class IndiGameUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    username = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        unique=True,
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'

    objects = IndiGameManager()


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30

    MALE = 'Male'
    FEMALE = 'Female'

    GENDERS = [(x, x) for x in (MALE, FEMALE)]

    email = models.EmailField(

    )

    username = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        unique=True,
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    profile_picture = models.ImageField(
        null=False,
        blank=False,

    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),
        choices=GENDERS,
        null=False,
        blank=False,
    )

    user = models.OneToOneField(
        IndiGameUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.username
