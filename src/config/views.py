from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Home page stub view
    """

    template_name = "home.html"
