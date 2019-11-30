from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from aggiehub.forms import LoginForm, PostForm
from aggiehub.models import User, Post, Notification, Claim

from toxicdetector import predict as predict

user = None

def home(request):
    if user is None:
        return redirect("login")
        
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.score = predict.getPredictions(post.text)
            post.save()
            if post.score > 0.5:
                notification = Notification(user = user, notif_id = post.id, type = Notification.TOXIC, text = post.text)
                notification.save()
            return redirect("home")
    else:
        posts = Post.objects.filter(score__lte = 0.5).order_by('-id')
        claims = user.claim_set.all()
        notifications = user.notification_set.all().order_by("-updated")
        surveys = user.survey_set.all()
        context = {"form": form, "user": user, "posts": posts, "notifications": notifications, "claims": claims, "surveys":surveys}
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
                return redirect("home")
            except User.DoesNotExist:
                context = {"form": LoginForm(None), "user": user}
                return render(request, "aggiehub/login.html", context)
    context = {"form": form, "user": user}
    return render(request, "aggiehub/login.html", context)


def logout(request):
    user = None
    return redirect("login")


def delete_post(request):
    post_id = request.GET.get('id', None)
    post = Post.objects.get(pk=post_id)
    post.delete()
    data = {
        'success': True
    }
    return JsonResponse(data)


def claim_post(request):
    post_id = request.GET.get('id', None)
    post = Post.objects.get(pk=post_id)
    exists = True

    if not post.claim_set.filter(user=user).exists():
        exists = False
        claim = Claim(post=post, user=user, resolved=False)
        claim.save()
        claim_type = Notification.CLAIM_TOXIC
        if post.user == user:
            claim_type = Notification.CLAIM_NONTOXIC
        notification = Notification(user = user, notif_id = claim.id, type = claim_type, text = post.text)
        notification.save()
    
    data = {
        'success': True,
        'exists': exists,
        'post': post.text,
        'claimType': claim_type
    }
    return JsonResponse(data)
