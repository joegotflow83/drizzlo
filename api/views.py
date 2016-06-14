from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from accounts.models import UserProfile
from cookbook.models import CookBook, Recipe, Ingredient, Instruction
from .serializers import CookBookSerializer, RecipeSerializer, IngredientSerializer, InstructionSerializer, \
        UserSerializer, UserProfileSerializer


class ListUsersAPI(generics.ListAPIView):
    """All users endpoint"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)


class RetrieveUpdateUserAPI(generics.RetrieveUpdateAPIView):
    """Single user endpoint"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs['pk'])


class ListUserProfilesAPI(generics.ListAPIView):
    """All userprofiles endpoint"""
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)


class RetrieveUpdateUserProfileAPI(generics.RetrieveUpdateAPIView):
    """Single userprofile endpoint"""
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserProfile.objects.filter(pk=self.kwargs['pk'])


########## CookBook APIs ###############


class ListCreateCookBooksAPI(generics.ListCreateAPIView):
    """All cookbooks endpoint"""
    serializer_class = CookBookSerializer
    queryset = CookBook.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        return super().create(request, *args, **kwargs)


class RetrieveUpdateCookBookAPI(generics.RetrieveUpdateAPIView):
    """Single Cookbook endpoint"""
    serializer_class = CookBookSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CookBook.objects.filter(pk=self.kwargs['pk'])


class ListRecipesAPI(generics.ListAPIView):
    """All recipes endpoint"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticated,)


class RetrieveUpdateRecipeAPI(generics.RetrieveUpdateAPIView):
    """Single recipe endpoint"""
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Recipe.objects.filter(pk=self.kwargs['pk'])


class ListIngredientsAPI(generics.ListAPIView):
    """All ingredients endpoint"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (IsAuthenticated,)


class RetrieveUpdateIngredientAPI(generics.RetrieveUpdateAPIView):
    """Single ingredient endpoint"""
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Ingredient.objects.filter(pk=self.kwargs['pk'])


class ListInstructionsAPI(generics.ListAPIView):
    """All instructions endpoint"""
    serializer_class = InstructionSerializer
    queryset = Instruction.objects.all()
    permission_classes = (IsAuthenticated,)


class RetrieveUpdateInstructionAPI(generics.RetrieveUpdateAPIView):
    """Single instruction endpoint"""
    serializer_class = InstructionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Instruction.objects.filter(pk=self.kwargs['pk'])
