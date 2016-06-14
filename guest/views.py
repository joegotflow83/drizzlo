from django.views.generic import TemplateView


class Index(TemplateView):
    """Initial landing page when a person accesses the site"""
    template_name = 'guest/index.html'

