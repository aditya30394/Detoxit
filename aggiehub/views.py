from django.http import HttpResponse
from django.shortcuts import redirect, render

from aggiehub.forms import LoginForm
from aggiehub.models import User


def home(request):
    return HttpResponse("Hello, Django!")


def login(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            email = form.save(commit=False).email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, "aggiehub/login.html", {"form": LoginForm(None)})
            return redirect("home")
    else:
        return render(request, "aggiehub/login.html", {"form": form})
