from django import forms
from aggiehub.models import User, Post
from django.forms import widgets

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("text", )

class SurveyForm(forms.Form):
    post_text = forms.CharField(label="Post", disabled=True)
    SCORE_CHOICES = zip(range(1, 6), range(1, 6))
    score = forms.ChoiceField(label="Score",choices=SCORE_CHOICES, widget=forms.RadioSelect)
    