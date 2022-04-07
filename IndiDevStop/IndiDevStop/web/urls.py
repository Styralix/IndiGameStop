from django.urls import path

from IndiDevStop.web.views import HomeView, AllGamesView, CreateGameView, GameDetailsView, \
    AllPostsView, CreatePostView, EditGameView, EditPostView, my_games, DeleteGameView, DeleteCommentView, \
    DeletePostView, LikeView

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('all/games/', AllGamesView.as_view(), name='all games'),
    path('my/games/', my_games, name='my games'),
    path('all/posts/', AllPostsView.as_view(), name='all posts'),
    path('add/game/', CreateGameView.as_view(), name='create game'),
    path('add/post/', CreatePostView.as_view(), name='create post'),
    path('game/details/<int:pk>/', GameDetailsView.as_view(), name='game details'),
    path('game/edit/<int:pk>/', EditGameView.as_view(), name='edit game'),
    path('post/edit/<int:pk>/', EditPostView.as_view(), name='edit post'),
    path('game/delete/<int:pk>/', DeleteGameView.as_view(), name='delete game'),
    path('comment/delete/<int:pk>/', DeleteCommentView.as_view(), name='delete comment'),
    path('post/delete/<int:pk>/', DeletePostView.as_view(), name='delete post'),
    path('game/like/<int:pk>/', LikeView, name='like game'),
)
