from django.db import models
from django.contrib.auth.models import User

from cookbook.models import Recipe
from final_project.custom_storages import MediaStorage


class Follower(models.Model):
    user = models.ForeignKey(User)
    the_following = models.ForeignKey(User, related_name="the_following")

    def __str__(self):
        return self.user.username


class Following(models.Model):
    user = models.ForeignKey(User)
    the_follower = models.ForeignKey(User, related_name="the_follower")

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    pic = models.ImageField("img", storage=MediaStorage(), null=True, blank=True)
    about_me = models.TextField(blank=True)
    followers = models.ManyToManyField(Follower, blank=True)
    following = models.ManyToManyField(Following, blank=True)
    is_confirmed = models.BooleanField(default=False)
    favorites = models.ManyToManyField(Recipe, blank=True)


class ActivateKey(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=36)
