from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from phonenumber_field.modelfields import PhoneNumberField
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


class EmailForm(forms.Form):
    name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    phone = PhoneNumberField(blank=True, null=True)
    email = forms.EmailField()
    to = forms.EmailField()
    text = forms.CharField(required=False, widget=forms.Textarea)

Tabnine::configStarted config server at http://127.0.0.1:5555/qgfxccplnzachvlwmmbb