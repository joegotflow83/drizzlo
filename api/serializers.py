from rest_framework import serializers
from django.contrib.auth.models import User

from accounts.models import UserProfile
from cookbook.models import CookBook, Recipe, Ingredient, Instruction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'about_me', 'followers', 'following', 'favorites']


class CookBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookBook


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
