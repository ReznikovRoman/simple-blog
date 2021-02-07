from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms
from . import models
from .decorators import (handle_authenticated_user, )


class SignUp(CreateView):
    """User-Signup view"""

    form_class = forms.CustomUserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'

    @handle_authenticated_user
    def get(self, request, *args, **kwargs):
        return super(SignUp, self).get(request, *args, **kwargs)


class LoginView(auth_views.LoginView):
    """User-Login view"""

    template_name = 'accounts/login.html'

    @handle_authenticated_user
    def get(self, request, *args, **kwargs):
        return super(LoginView, self).get(request, *args, **kwargs)


class EditUserProfile(LoginRequiredMixin, UpdateView):
    """Update profile view"""
    model = models.Profile
    form_class = forms.ProfileUpdateForm
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



















