from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from IndiDevStop.web.forms import CreateGameForm, CommentForm, CreatePostForm, EditGameForm, EditPostForm, \
    DeleteGameForm, DeleteCommentForm, DeletePostForm
from IndiDevStop.web.models import Game, Post, Comment


class HomeView(views.ListView):
    template_name = 'home.html'
    model = Game
    context_object_name = 'games'
    paginate_by = 3


class AllGamesView(views.ListView):
    model = Game
    template_name = 'all_games.html'
    context_object_name = 'games'


class AllPostsView(views.ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'


def my_games(request):
    current_user = request.user

    if current_user.id:
        user_games = Game.objects.filter(user=current_user)
        return render(request, 'my_games.html', {'games': user_games})
    else:
        return render(request, 'my_games.html')


class CreateGameView(LoginRequiredMixin, views.CreateView):
    template_name = 'create_game.html'
    form_class = CreateGameForm
    success_url = reverse_lazy('all games')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CreatePostView(LoginRequiredMixin, views.CreateView):
    template_name = 'create_post.html'
    form_class = CreatePostForm
    success_url = reverse_lazy('all posts')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class GameDetailsView(views.DetailView):
    model = Game
    template_name = 'game_details.html'
    slug_field = 'slug'

    form = CommentForm

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()

            return HttpResponseRedirect(reverse('game details', args=[str(post.pk)]))

    def get_context_data(self, **kwargs):
        post_comments = Comment.objects.all().filter(post=self.object.id)
        context = super().get_context_data(**kwargs)

        stuff = get_object_or_404(Game, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context.update({
            'form': self.form,
            'post_comments': post_comments,
            'total_likes': total_likes,
            'liked': liked,
        })
        return context


class EditGameView(LoginRequiredMixin, views.UpdateView):
    model = Game
    template_name = 'edit_game.html'
    form_class = EditGameForm

    def get_success_url(self):
        return reverse_lazy('game details', kwargs={'pk': self.object.id})


class EditPostView(LoginRequiredMixin, views.UpdateView):
    model = Post
    template_name = 'edit_post.html'
    form_class = EditPostForm

    def get_success_url(self):
        return reverse_lazy('all posts')


class DeleteGameView(LoginRequiredMixin, views.DeleteView):
    model = Game
    template_name = 'delete_game.html'
    form_class = DeleteGameForm
    success_url = reverse_lazy('all games')


class DeleteCommentView(LoginRequiredMixin, views.DeleteView):
    model = Comment
    template_name = 'delete_comment.html'
    form_class = DeleteCommentForm

    success_url = reverse_lazy('all games')


class DeletePostView(LoginRequiredMixin, views.DeleteView):
    model = Post
    template_name = 'delete_post.html'
    form_class = DeletePostForm
    success_url = reverse_lazy('all posts')


def LikeView(request, pk):
    game = get_object_or_404(Game, id=request.POST.get('game_id'))
    liked = False

    if game.likes.filter(id=request.user.id).exists():
        game.likes.remove(request.user)
        liked = False
    else:
        game.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('game details', args=[str(pk)]))


class ErrorView(views.View):
    def get(self, request):
        return HttpResponse('<h4>Some Strange Error Has Occurred</h4>')


class Error404View(views.View):
    def get(self, request):
        return HttpResponse('<h4>The Page You Are Looking For Might Not Exist</h4>')
