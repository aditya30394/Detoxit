from django.http import HttpResponse
from django.shortcuts import redirect, render

from aggiehub.forms import LoginForm
from aggiehub.models import User

user = None


def home(request):
    if user is None:
        return redirect("login")
    posts = user.post_set.order_by('-id')
    return render(request, "aggiehub/home.html", {"user": user, "posts": posts})


def login(request):
    form = LoginForm(request.POST or None)
    global user
    user = None
    if request.method == "POST":
        if form.is_valid():
            email = form.save(commit=False).email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                context = {"form": LoginForm(None), "user": user}
                return render(request, "aggiehub/login.html", context)
            return redirect("home")
    else:
        context = {"form": form, "user": user}
        return render(request, "aggiehub/login.html", context)


def logout(request):
    user = None
    return redirect("login")
