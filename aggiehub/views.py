from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from aggiehub.forms import LoginForm, PostForm
from aggiehub.models import User, Post

user = None


def home(request):
    if user is None:
        return redirect("login")
        
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()
            return redirect("home")
    else:
        posts = Post.objects.order_by('-id')
        claims = user.claim_set.all()
        context = {"form": form, "user": user, "posts": posts, "claims": claims}
        return render(request, "aggiehub/home.html", context)


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


def delete_post(request):
    id = request.GET.get('id', None)
    post = Post.objects.get(pk=id)
    post.delete()
    data = {
        'success': True
    }
    return JsonResponse(data)


def claim_post(request):
    id = request.GET.get('id', None)
    post = Post.objects.get(pk=id)
    exists = True

    if not post.claim_set.filter(user=user).exists():
        exists = False
        post.claim_set.create(user=user, resolved=False)
    
    data = {
        'success': True,
        'exists': exists,
        'post': post.text
    }
    return JsonResponse(data)