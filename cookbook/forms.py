from django import forms

from .models import Comment, Recipe, CookBook


class CookBookForm(forms.ModelForm):
    class Meta:
        model = CookBook
        fields = ('name',)


class RecipeForm(forms.Form):
    title = forms.CharField(
            widget=forms.TextInput(attrs={
                'placeholder': 'Name',
                }))
    image = forms.ImageField()
    prep_time = forms.IntegerField(
            widget=forms.TextInput(attrs={
                'placeholder': 'Enter in min',
                }))
    cook_time = forms.IntegerField(
            widget=forms.TextInput(attrs={
                'placeholder': 'Enter in min',
                }))
    tags = forms.CharField(
            widget=forms.TextInput(attrs={
                'placeholder': 'Enter tags',
                }))

    def save(self):
        data = self.cleaned_data
        Recipe.objects.create(
                title=data['title'],
                image=data['image'],
                prep_time=data['prep_time'],
                cook_time=data['cook_time'],
                tags=data['tags'],
                )


class IngredientForm(forms.Form):
    ingredient = forms.CharField(
           widget=forms.TextInput(attrs={
                   'placeholder': 'Enter Ingredient',
                   }))


class InstructionForm(forms.Form):
    direction = forms.CharField(
            widget=forms.TextInput(attrs={
                'placeholer': 'Enter Instruction',
                }))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('response',)


