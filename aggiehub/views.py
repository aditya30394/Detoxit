from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from aggiehub.forms import LoginForm, PostForm
from aggiehub.models import User, Post, Notification, Claim

from toxicdetector import naive_predict as naive_predict

from aggiehub.forms import LoginForm, PostForm, SurveyForm
from aggiehub.models import User, Post, Notification, Claim, Survey
from toxicdetector import naive_predict as naive_predict

from toxicdetector import predict as predict
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
                toxic_words = naive_predict.predict_each_word(post.text)
                toxic_words = ' ,'.join(toxic_words)
                notification = Notification(user = user, notif_id = post.id, type = Notification.TOXIC, text = post.text, toxic_words = toxic_words)
                notification.save()
            return redirect("home")
    else:
        posts = Post.objects.filter(score__lte = 0.5).order_by('-id')
        claims = user.claim_set.all()
        
        already_claimed_posts = []
        for claim in claims:
            if claim.post in posts:
                already_claimed_posts.append(claim.post)

        notifications = user.notification_set.all().order_by("-updated")
        surveys = user.survey_set.filter(is_completed__exact = False)
        context = {"form": form, "user": user, "posts": posts, "notifications": notifications, "claims": claims, "surveys":surveys, "already_claimed_posts":already_claimed_posts}
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
    claim_type = Notification.CLAIM_TOXIC
    if not post.claim_set.filter(user=user).exists():
        exists = False
        claim = Claim(post=post, user=user, resolved=False)
        claim.save()
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

def survey(request, sid):
    logger.error(request)
    
    form = SurveyForm(request.POST or None)
    
    if request.method == "POST":
        
        return redirect("home")
    else:
        survey = Survey.objects.get(id=sid)
        form = SurveyForm(auto_id=False, initial={'post_text': survey.post.text})
        context = {"form": form, "id": sid, "survey":survey }
        return render(request, "aggiehub/survey.html", context)