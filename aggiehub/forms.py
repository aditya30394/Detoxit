from django import forms
from aggiehub.models import User


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", )
