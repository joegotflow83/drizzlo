from django.conf.urls import url

from api import views


urlpatterns = [
    url(r'^users/$', views.ListUsersAPI.as_view(), name='list_users_api'),
    url(r'^user/(?P<pk>\d+)/$', views.RetrieveUpdateUserAPI.as_view(), name='retrieve_update_users_api'),
    url(r'^userprofiles/$', views.ListUserProfilesAPI.as_view(), name='list_userprofiles_api'),
    url(r'^userprofile/(?P<pk>\d+)/$', views.RetrieveUpdateUserProfileAPI.as_view(), name='retrieve_update_userprofiles_api'),
    url(r'^cookbooks/$', views.ListCreateCookBooksAPI.as_view(), name='list_cookbooks_api'),
    url(r'^cookbook/(?P<pk>\d+)/$', views.RetrieveUpdateCookBookAPI.as_view(), name='retrieve_update_cookbooks_api'),
    url(r'^recipes/$', views.ListRecipesAPI.as_view(), name='list_recipes_api'),
    url(r'^recipe/(?P<pk>\d+)/$', views.RetrieveUpdateRecipeAPI.as_view(), name='retrieve_update_recipes_api'),
    url(r'^ingredients/$', views.ListIngredientsAPI.as_view(), name='list_ingredients_api'),
    url(r'^ingredient/(?P<pk>\d+)/$', views.RetrieveUpdateIngredientAPI.as_view(), name='retrieve_update_ingredients_api'),
    url(r'^instructions/$', views.ListInstructionsAPI.as_view(), name='list_instructions_api'),
    url(r'^instruction/(?P<pk>\d+)/$', views.RetrieveUpdateInstructionAPI.as_view(), name='retrieve_update_instructions_api'),
]
