from django import forms

from IndiDevStop.common.helpers import DisabledFieldsFormMixin
from IndiDevStop.web.models import Game, Comment, Post


class CreateGameForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        game = super().save(commit=False)

        game.user = self.user
        if commit:
            game.save()

        return game

    class Meta:
        model = Game
        fields = ('title', 'picture', 'description', 'type', 'release_date', 'download_link',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Game name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Short description of the game'}),
            'release_date': forms.DateInput(attrs={'placeholder': 'Year-Month-Day'}),
            'download_link': forms.URLInput(attrs={'placeholder': 'Download link'}),
        }


class CreatePostForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        post = super().save(commit=False)

        post.user = self.user
        if commit:
            post.save()

        return post

    class Meta:
        model = Post
        fields = ('title', 'body')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post name'}),
            'body': forms.Textarea(attrs={'placeholder': 'What is on your mind?'}),
        }



class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Add a comment...',
        })
    )

    class Meta:
        model = Comment
        fields = ('content',)


class EditGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('title', 'picture', 'description', 'type', 'release_date', 'download_link',)


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body',)


class DeleteGameForm(DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_disabled_fields()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Game
        exclude = ('title', 'picture', 'likes', 'description', 'type', 'release_date', 'download_link', 'user')


class DeleteCommentForm(DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_disabled_fields()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Comment
        exclude = ('content', 'post', 'user', 'date', )


class DeletePostForm(DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_disabled_fields()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Post
        exclude = ('title', 'body', 'date_added', 'user', )
