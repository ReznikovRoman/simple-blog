
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . import models


####################################################################################################################


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = models.CustomUser

    def __init__(self, *args, **kwargs):
        super(CustomUserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Create a username'
        self.fields['email'].label = 'Email address'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('bio', 'profile_pic', 'uplay_nickname')

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'input_field'}),
            'uplay_nickname': forms.TextInput(attrs={'class': 'input_field'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        self.fields['bio'].label = 'Write something about experience with Anno series'
        self.fields['profile_pic'].label = 'Upload your profile picture'
        self.fields['uplay_nickname'].label = 'Enter your Uplay nickname'











