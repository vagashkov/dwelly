from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from ..models import Profile


class DisplayProfile(LoginRequiredMixin, DetailView):
    """
    Manages user profile display option
    """
    template_name = "users/display_profile.html"
    context_object_name = "profile"

    def get_object(self, queryset: QuerySet = None) -> Profile:
        return self.request.user.profile


class EditProfile(LoginRequiredMixin, UpdateView):
    """
    Manages user profile edit option
    """
    template_name = "users/edit_profile.html"
    fields = [
        Profile.Field.photo,
        Profile.Field.first_name,
        Profile.Field.last_name,
        Profile.Field.phone,
        Profile.Field.bio,
    ]
    success_url = reverse_lazy("user_display_profile")

    def get_object(self, queryset: QuerySet = None) -> Profile:
        return self.request.user.profile
