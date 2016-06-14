from django.views.generic import TemplateView

from cookbook.models import Recipe


class Dashboard(TemplateView):
    """Display info of users that the particular user is following"""
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_following = self.request.user.userprofile.following.all()
        context['top_rated'] = Recipe.objects.all().order_by('-favorites_num')[:5]
        for person in user_following:
            print(person.user.recipe_set.last())
        print(user_following.count())
        if user_following.count() == 0:
            print('here')
            context['no_one'] = True
            return context
        else:
            context['people'] = user_following
            return context
