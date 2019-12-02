from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=70, blank=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=140)
    score = models.FloatField(default=None)

    def __str__(self):
        return self.text
    
    def isToxic(self):
        return True if self.score > 0.5 else False


class Claim(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resolved = models.BooleanField(default=False)


class Notification(models.Model):
    CLAIM_TOXIC = 'CLAIM_TOXIC'
    CLAIM_NONTOXIC = 'CLAIM_NONTOXIC'
    RESOLVE_TOXIC = 'RESOLVE_TOXIC'
    RESOLVE_NONTOXIC = 'RESOLVE_NONTOXIC'
    TOXIC = 'TOXIC'
    NOTIF_CHOICES = [
        (CLAIM_TOXIC, 'Claim Toxic'),
        (CLAIM_NONTOXIC, 'Claim Non-Toxic'),
        (RESOLVE_TOXIC, 'Resolve Toxic'),
        (RESOLVE_NONTOXIC, 'Resolve Non-Toxic'),
        (TOXIC, 'Toxic'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=140)
    toxic_words =  models.CharField(max_length=50)
    type = models.CharField(
        max_length=20,
        choices=NOTIF_CHOICES,
        default=TOXIC,
    )
    notif_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Survey(models.Model):
    SCORE_CHOICES = zip(range(1, 6), range(1, 6))
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=SCORE_CHOICES, blank=True, null=True)
    is_completed = models.BooleanField(default=False)
