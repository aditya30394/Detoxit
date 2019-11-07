from django import forms
from aggiehub.models import User, Post


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text", )
