from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from blog.models import BlogUser, Comment, Post, Album


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


class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]


class SearchBoxForm(forms.Form):
    q = forms.CharField()


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = []

    zip = forms.FileField(required=False)


class ContactForm(forms.Form):
    email = forms.EmailField(
        required=True,
        max_length=254,
        widget=forms.EmailInput(
            attrs={'class': 'form-control form-control-lg'}
        )
    )
    phone = forms.CharField(
        required=False,
        max_length=254,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg'}
        )
    )
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Write your name here'
            }
        )
    )
    subject = forms.CharField(
        required=False,
        max_length=254,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg'}
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '10',
                'cols': '30',

            }
        ),
        required=True
    )
