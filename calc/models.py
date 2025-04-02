import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Team(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')
    num_allrounders = models.IntegerField(default=0)
    num_batsmen = models.IntegerField(default=0)
    num_bowlers = models.IntegerField(default=0)
    unique_link = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def get_shareable_link(self):
        return reverse('player_form', kwargs={'unique_link': self.unique_link})

    def __str__(self):
        return self.name

class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    role = models.CharField(max_length=20)
    wickets_taken = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
    batting_high_score = models.IntegerField(default=0)
    total_runs = models.IntegerField(default=0)
    strike_rate = models.FloatField(default=0.0)
    fifties = models.IntegerField(default=0)
    hundreds = models.IntegerField(default=0)
    economy_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    num_bowlers = models.IntegerField(default=0)
    num_batsmen = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    unique_link = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def get_shareable_link(self):
        return reverse('player_form_view', kwargs={'unique_link': self.unique_link})

    def __str__(self):
       return self.user.username

