from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from accounts import views


urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^verify/$', require_POST(views.Verify.as_view()), name='verify'),
    url(r'^verify/success/$', views.SuccessVerify.as_view(), name='success_verify'),
    url(r'^signup/$', views.Signup.as_view(), name='signup'),
    url(r'^logout/$', login_required(auth_views.logout_then_login), name='logout'),
    url(r'^profile/$', login_required(views.OwnProfile.as_view()), name='own_profile'),
    url(r'^profile/(?P<pk>\d+)/$', login_required(views.Profile.as_view()), name='profile'),
    url(r'^update/profile/(?P<pk>\d+)/$', login_required(views.UpdateProfile.as_view()), name='update_profile'),
    url(r'^search/$', login_required(views.SearchUsers.as_view()), name='search_users'),
    url(r'^follow/(?P<pk>\d+)/$', login_required(views.StartFollow.as_view()), name='follow'),
    url(r'^profile/followers/(?P<pk>\d+)/$', login_required(views.DisplayFollowers.as_view()), name='display_followers'),
    url(r'^profile/following/(?P<pk>\d+)/$', login_required(views.DisplayFollowing.as_view()), name='display_following'),
    url(r'^user/cookbooks/(?P<pk>\d+)/$', login_required(views.DisplayCookBooks.as_view()), name='display_cookbooks'),
    url(r'^profile/shopping/list/$', views.DisplayShoppingList.as_view(), name='display_shopping_list'),
    url(r'^profile/shopping/list/delete/item/(?P<pk>\d+)/$', views.DeleteItem.as_view(), name='delete_item'),
    url(r'^unfollow/(?P<pk>\d+)/$', views.UnFollow.as_view(), name='unfollow'),
    url(r'^send/sms/$', views.SendSMS.as_view(), name='send_sms'),
]
