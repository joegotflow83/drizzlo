from django.db import models
from django.contrib.auth.models import User

from final_project.custom_storages import MediaStorage


class Favorite(models.Model):
    user = models.ForeignKey(User)


class Item(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    user = models.OneToOneField(User)
    items = models.ManyToManyField(Item, blank=True)


class CookBook(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)


class Comment(models.Model):
    user = models.ForeignKey(User)
    response = models.TextField()


class Recipe(models.Model):
    user = models.ForeignKey(User)
    cookbook = models.ForeignKey(CookBook)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="img", storage=MediaStorage(), blank=True, null=True)
    favorites = models.ManyToManyField(Favorite)
    favorites_num = models.IntegerField(default=0)
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    tags = models.TextField(blank=True, null=True)
    comments = models.ManyToManyField(Comment, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    ingredient = models.TextField(max_length=255)


class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe)
    direction = models.TextField()

