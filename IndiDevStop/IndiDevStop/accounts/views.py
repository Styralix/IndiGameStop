from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic as views
from django.contrib.auth import views as auth_views, login
from django.urls import reverse_lazy

from IndiDevStop.accounts.forms import CreateProfileForm, EditProfileForm
from IndiDevStop.accounts.models import Profile


class UserRegisterView(views.CreateView):
    form_class = CreateProfileForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserLogoutView(auth_views.LogoutView):
    pass


class ProfileDetailsView(LoginRequiredMixin, views.DetailView):
    model = Profile
    template_name = 'profile_details.html'
    context_object_name = 'profile'


class EditProfileView(LoginRequiredMixin, views.UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    form_class = EditProfileForm

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.object.pk})
