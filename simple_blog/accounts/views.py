from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreateForm, ProfileUpdateForm
from .models import Profile
from .decorators import restrict_authenticated_users


class SignUp(CreateView):
    """User-Signup view."""
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'

    @restrict_authenticated_users
    def get(self, request, *args, **kwargs):
        return super(SignUp, self).get(request, *args, **kwargs)


class LoginView(auth_views.LoginView):
    """User-Login view."""
    template_name = 'accounts/login.html'

    @restrict_authenticated_users
    def get(self, request, *args, **kwargs):
        return super(LoginView, self).get(request, *args, **kwargs)


class EditUserProfile(LoginRequiredMixin, UpdateView):
    """Update profile view."""
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_initial(self):
        return {
            'bio': self.request.user.profile.bio,
            'profile_pic': self.request.user.profile.profile_pic,
            'uplay_nickname': self.request.user.profile.uplay_nickname,
        }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user.profile = self.request.user.profile
        self.object.save()
        return super(EditUserProfile, self).form_valid(form)
