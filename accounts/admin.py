from django.contrib import admin

from .models import UserProfile, Follower, Following, ActivateKey


admin.site.register([UserProfile, Follower, Following, ActivateKey])
