from django.urls import path

from IndiDevStop.accounts.views import UserLoginView, UserRegisterView, UserLogoutView, ProfileDetailsView, \
    EditProfileView

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('edit/profile/<int:pk>/', EditProfileView.as_view(), name='edit profile'),
)
