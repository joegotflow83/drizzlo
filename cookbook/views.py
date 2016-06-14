from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, View
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User

from .models import CookBook, Recipe, Comment, Ingredient, Instruction, Item, Favorite
from .forms import RecipeForm, CommentForm, IngredientForm, InstructionForm, CookBookForm
from accounts.tasks import send_recipe_email


class CreateCookBook(CreateView):
    """Allow a user to create a new cookbook"""
    template_name = 'cookbook/cookbook_list.html'
    model = CookBook
    fields = ['name']

    def form_valid(self, form):
        new_cookbook = form.save(commit=False)
        new_cookbook.user = self.request.user
        new_cookbook.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('list_cookbooks')


class ListCookBooks(ListView):
    """List a users cookbooks that they have created"""
    model = CookBook

    def get_queryset(self):
        return CookBook.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = self.request.user.userprofile.favorites.all()
        context['form'] = CookBookForm
        return context


def create_recipe(request, pk):
    """Users can create their own recipes"""
    recipeform = RecipeForm()
    IngredientFormSet = formset_factory(IngredientForm)
    InstructionFormSet = formset_factory(InstructionForm)
    cookbook = CookBook.objects.get(pk=pk)
    if request.method == "POST":
        recipeform = RecipeForm(request.POST, request.FILES)
        ingredientformset = IngredientFormSet(request.POST)
        instructionformset = InstructionFormSet(request.POST)
        if recipeform.is_valid() and ingredientformset.is_valid() and instructionformset.is_valid():
            new_ingredients = []
            picture = recipeform['image']
            for letter in picture:
                if letter in [' ', '20', '%']:
                    letter.replace(letter, '_')
            new_recipe = Recipe(
                    user=request.user,
                    cookbook=cookbook,
                    title=recipeform.cleaned_data['title'],
                    image=picture,
                    prep_time=recipeform.cleaned_data['prep_time'],
                    cook_time=recipeform.cleaned_data['cook_time'],
                    tags=recipeform.cleaned_data['tags'],
            )
            new_recipe.save()
            for ingredient_form in ingredientformset:
                description = ingredient_form.cleaned_data['ingredient']
                if ingredient_form:
                    new_ingredients.append(Ingredient.objects.create(recipe=new_recipe, ingredient=description))
            Instruction.objects.create(recipe=new_recipe, direction=request.POST.get('direction'))
        return HttpResponseRedirect(reverse('list_cookbooks'))
    else:
        recipe_form = RecipeForm()
        ingredient_form_set = IngredientFormSet()
        instruction_form_set = InstructionFormSet()
        return render(request, 'cookbook/recipe_form.html', {'recipe_form': recipe_form,
                                                             'ingredient_formset': ingredient_form_set,
                                                             'instruction_formset': instruction_form_set})


class ListRecipes(ListView):
    """List all the recipes for a particular cookbook"""
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cookbook_pk'] = self.kwargs['pk']
        first_half = Recipe.objects.filter(cookbook=self.kwargs['pk']).count()
        if first_half % 2 == 0:
            context['first_recipes'] = Recipe.objects.filter(cookbook=self.kwargs['pk'])[:first_half/2]
            context['last_recipes'] = Recipe.objects.filter(cookbook=self.kwargs['pk'])[first_half/2:]
        else:
            context['first_recipes'] = Recipe.objects.filter(cookbook=self.kwargs['pk'])[:(first_half/2)+1]
            context['last_recipes'] = Recipe.objects.filter(cookbook=self.kwargs['pk'])[first_half/2:]
        return context

    def get_queryset(self):
        return Recipe.objects.filter(cookbook=self.kwargs['pk'])


class DetailRecipe(DetailView):
    """View a recipe in detail with all info"""
    model = Recipe

    def get_context_data(self, **kwargs):
        """Display comment form which users can comment on recipes"""
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        return context


class SendRecipeEmail(View):
    """Send the user an email of the recipe"""
    def get(self, request, recipe_pk, creator_pk):
        recipe = Recipe.objects.get(pk=recipe_pk)
        ingredients = Ingredient.objects.filter(recipe=recipe)
        instructions = Instruction.objects.filter(recipe=recipe)
        ingredients_list = ['{}. {}'.format((index + 1), ingredient.ingredient) for index, ingredient in enumerate(ingredients)]
        instruction_list = ['{}. {}'.format((index + 1), instruction.direction) for index, instruction in enumerate(instructions)]
        ingredients_list = ', '.join(ingredients_list)
        instruction_list = ', '.join(instruction_list)
        user = User.objects.get(pk=creator_pk)
        send_recipe_email.delay(recipe.pk, request.user.pk, user.username, ingredients_list, instruction_list)
        return HttpResponseRedirect(reverse('detail_recipe', kwargs={'pk': recipe_pk}))


class Comment(CreateView):
    """Allow a user to create a comment on a recipe"""
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        new_comment = form.save(commit=False)
        new_comment.user = self.request.user
        new_comment.save()
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        recipe.comments.add(new_comment)
        recipe.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_recipe', kwargs={'pk': self.kwargs['pk']})


class SaveRecipe(View):
    """Users can save recipes"""
    def get(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        user = request.user
        user.userprofile.favorites.add(recipe)
        return HttpResponseRedirect(reverse('list_cookbooks'))


class AddFavorite(View):
    """Users can favorite recipes"""
    def get(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        favorites = recipe.favorites.all()
        for favorite in favorites:
            if favorite.user == request.user:
                return HttpResponseRedirect(reverse('detail_recipe', kwargs={'pk': pk}))
        favorite = Favorite(user=request.user)
        favorite.save()
        recipe.favorites.add(favorite)
        recipe.favorites_num += 1
        recipe.save()
        return HttpResponseRedirect(reverse('detail_recipe', kwargs={'pk': pk}))


class AddItem(View):
    """Users can add items to their shopping cart"""
    def get(self, request, item, pk):
        new_item = Item(name=item)
        new_item.save()
        user = self.request.user
        user.shoppinglist.items.add(new_item)
        user.shoppinglist.save()
        return HttpResponseRedirect(reverse('detail_recipe', kwargs={'pk': pk}))
