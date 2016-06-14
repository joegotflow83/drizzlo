from django.contrib import admin

from .models import Recipe, Ingredient, Instruction, CookBook, ShoppingList


admin.site.register([CookBook, Recipe, Ingredient, Instruction, ShoppingList])
