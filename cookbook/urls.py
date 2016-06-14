from django.conf.urls import url
from django.views.decorators.http import require_POST

from cookbook import views


urlpatterns = [
    url(r'^create/$', require_POST(views.CreateCookBook.as_view()), name='create_cookbook'),
    url(r'^$', views.ListCookBooks.as_view(), name='list_cookbooks'),
    url(r'^recipes/list/(?P<pk>\d+)/$', views.ListRecipes.as_view(), name='list_recipes'),
    url(r'^recipes/create/(?P<pk>\d+)/$', views.create_recipe, name='create_recipe'),
    url(r'^recipe/(?P<pk>\d+)/$', views.DetailRecipe.as_view(), name='detail_recipe'),
    url(r'^recipe/(?P<recipe_pk>\d+)/(?P<creator_pk>\d+)/$', views.SendRecipeEmail.as_view(), name='send_recipe_email'),
    url(r'^comment/create/(?P<pk>\d+)/$', require_POST(views.Comment.as_view()), name='comment'),
    url(r'^recipe/save/recipe/(?P<pk>\d+)/$', views.SaveRecipe.as_view(), name='save_recipe'),
    url(r'^recipe/favorite/(?P<pk>\d+)/$', views.AddFavorite.as_view(), name='favorite'),
    url(r'^shopping/list/add/(?P<item>.*)/(?P<pk>\d+)/$', views.AddItem.as_view(), name='add_item'),
]
