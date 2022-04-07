from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from IndiDevStop.accounts.models import Profile


class CreateProfileForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,

    )

    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
    )

    username = forms.CharField(
        max_length=30,
    )

    profile_picture = forms.ImageField()

    email = forms.EmailField()

    gender = forms.ChoiceField(
        choices=Profile.GENDERS,
    )

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            profile_picture=self.cleaned_data['profile_picture'],
            user=user,
        )

        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'profile_picture')


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = ('email', 'username', 'first_name', 'last_name', 'description', 'gender', 'profile_picture')
