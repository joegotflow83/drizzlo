from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView, View, ListView
from rest_framework.authtoken.models import Token
import urllib.parse

from .tasks import send_verify_email, send_sms
from .forms import UserForm, VerifyForm, ProfileForm
from .models import Follower, Following, UserProfile, ActivateKey
from cookbook.models import Recipe, Item, ShoppingList


class Signup(CreateView):
    """Allow a user to sign up"""
    model = User
    form_class = UserForm

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.email = form.cleaned_data['email']
        new_user.save()
        UserProfile.objects.create(user=new_user)
        ShoppingList.objects.create(user=new_user)
        Token.objects.create(user=new_user)
        send_verify_email.delay(new_user.pk)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('login')


class Verify(FormView):
    """Verify the email the user has given"""
    template_name = 'accounts/verify.html'
    model = ActivateKey
    form_class = VerifyForm

    def form_valid(self, form):
        new_key = form.save(commit=False)
        key = ActivateKey.objects.get(user=self.request.user)
        if new_key.key == key.key:
            self.request.user.userprofile.is_confirmed = True
            self.request.user.userprofile.save()
            key.delete()
            return super().form_valid(form)
        else:
            return render(self.request, 'error/verify.html')

    def get_success_url(self):
        return reverse('success_verify')


class SuccessVerify(TemplateView):
    """Inform the user that there verification was successful"""
    template_name = 'success/verify.html'


class OwnProfile(TemplateView):
    """Display a users info"""
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VerifyForm
        context['token'] = Token.objects.get(user=self.request.user)
        context['shopping_list'] = self.request.user.shoppinglist.items.all()
        return context


class Profile(DetailView):
    """Display another users info"""
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.filter(user=self.kwargs['pk'])
        user_following = self.request.user.userprofile.following.all()
        user_to_follow = User.objects.get(pk=self.kwargs['pk'])
        for person in user_following:
            if person.user == user_to_follow:
                context['follow'] = True
            else:
                context['false'] = False
        return context


class SearchUsers(TemplateView):
    """Allow users to search for other users"""
    template_name = 'accounts/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query', False)
        context['users'] = User.objects.filter(username=query).exclude(username=self.request.user)
        context['type'] = Recipe.objects.filter(tags=query)
        return context


class StartFollow(View):
    """Start following someone"""
    def get(self, request, pk):
        user = User.objects.get(pk=self.kwargs['pk'])
        new_follower = Follower.objects.create(user=request.user, the_following=user)
        user.userprofile.followers.add(new_follower)
        active_user = request.user
        new_following = Following.objects.create(user=user, the_follower=active_user)
        active_user.userprofile.following.add(new_following)
        return HttpResponseRedirect(reverse('own_profile'))


class UnFollow(View):
    """Unfollow someone"""
    def get(self, request, pk):
        session_user = request.user
        following_user = Following.objects.get(user=self.kwargs['pk'], the_follower=session_user)
        user = User.objects.get(pk=self.kwargs['pk'])
        follower_user = Follower.objects.get(user=request.user, the_following=user)
        session_user.userprofile.following.remove(following_user)
        user.userprofile.followers.remove(follower_user)
        return HttpResponseRedirect(reverse('own_profile'))


class DisplayFollowers(DetailView):
    """Display a list of users following a particular user"""
    template_name = 'accounts/followers.html'
    model = User


class DisplayFollowing(DetailView):
    """Display a list of users that user is following in particular"""
    template_name = 'accounts/following.html'
    model = User


class DisplayCookBooks(ListView):
    """Display that users cookbooks they have created"""
    template_name = 'accounts/recipe_list.html'
    model = Recipe

    def get_queryset(self):
        return Recipe.objects.filter(user=self.kwargs['pk'])


class UpdateProfile(UpdateView):
    """User can update their profile info"""
    model = UserProfile
    form_class = ProfileForm

    def form_valid(self, form):
        update_form = form.save(commit=False)
        picture = update_form.pic
        for letter in picture:
            if letter in [' ', '20', '%']:
                letter.replace(letter, '_')
        UserProfile.objects.filter(user=self.request.user).update(pic=picture)
        UserProfile.objects.filter(user=self.request.user).update(about_me=update_form.about_me)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('own_profile')


class DisplayShoppingList(TemplateView):
    """Show a users shopping list"""
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shopping_list'] = self.request.user.shoppinglist.items.all()
        return context


class DeleteItem(View):
    """Users can delete items off their shopping list"""
    def get(self, request, pk):
        item = Item.objects.get(pk=self.kwargs['pk'])
        item.delete()
        return HttpResponseRedirect(reverse('display_shopping_list'))


class SendSMS(View):
    """Send a text message to the user of their shopping list"""
    def post(self, request):
        number = request.POST['number']
        user_shopping_list = request.user.shoppinglist.items.all()
        shoppinglist = [item.name for item in user_shopping_list]
        shoppinglist = ', '.join(shoppinglist)
        send_sms.delay(shoppinglist, number)
        return HttpResponseRedirect(reverse('own_profile'))
