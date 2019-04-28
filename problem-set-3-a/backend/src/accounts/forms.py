from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
  email = forms.EmailField(
        label=_("Email"),
    )

  class Meta:
    model = User
    fields = ("username", "email")
    field_classes = {'username': UsernameField}
