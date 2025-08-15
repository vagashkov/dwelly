from django.views.generic import ListView, DetailView

from core.models import BaseModel
from .models import Listing


class List(ListView):
    """
    Retrieves listing short descriptions list
    """

    model = Listing
    ordering = BaseModel.Field.created_at
    # paginate_by = 1
    template_name = "listings/list.html"
    context_object_name = "listings"


class Details(DetailView):
    """
    Retrieves single listing details data
    """

    model = Listing
    template_name = "listings/details.html"
