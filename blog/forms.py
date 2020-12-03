from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from blog.models import BlogUser


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False,
        help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False,
        help_text='Optional.')
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.')

    tg_name = forms.CharField(
        max_length=30, required=False,
        help_text='Optional.')

    class Meta:
        model = BlogUser
        fields = ('username', 'first_name', 'last_name',
                  'email', 'tg_name', 'password1', 'password2',)
