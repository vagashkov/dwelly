from django.http import (
    HttpRequest, HttpResponse, Http404, HttpResponseRedirect
)
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View, ListView

from core.models import BaseModel

from .constants import ERROR_MSG_UNKNOWN_LISTING
from .forms import ReservationForm
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


class Details(View):
    """
    Retrieves single listing details data
    """

    model = Listing
    template_name = "listings/details.html"

    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        """
        Displays selected listing details in common with reservation form
        :param request:
        :param slug:
        :return:
        """

        try:
            context: dict = {
                "listing": self.model.objects.get(
                    slug=slug
                ),
                "reservation_form": ReservationForm()
            }
            return render(
                request,
                self.template_name,
                context
            )
        except Listing.DoesNotExist:
            raise Http404(
                ERROR_MSG_UNKNOWN_LISTING.format(
                    slug
                )
            )

    def post(self, request: HttpRequest, slug: str) -> HttpResponse:
        """
        Processing new listing reservation
        :param self:
        :param request:
        :param slug
        :return:
        """

        current_listing = self.model.objects.get(slug=slug)
        reservation_form = ReservationForm(request.POST)

        # if form valid - save it and return to post page
        if reservation_form.is_valid():
            reservation = ReservationForm.save(commit=False)
            reservation.author = request.user
            reservation.listing = current_listing
            reservation.save()
            return HttpResponseRedirect(
                reverse(
                    "listings:listing_details",
                    args=[
                        slug
                    ]
                )
            )

        # if form isn't valid - reload post page with form errors included
        context = {
            "listing": current_listing,
            "reservation_form": reservation_form
        }
        return render(
            request,
            self.template_name,
            context
        )
