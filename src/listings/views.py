from django.conf import settings
from django.http import (
    HttpRequest, HttpResponse,
    HttpResponseForbidden, Http404, HttpResponseRedirect
)
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, ListView

from core.models import BaseModel

from .constants import ERROR_MSG_UNKNOWN_LISTING
from .forms import ReservationForm
from .models import Listing, Reservation, ReservationStatus


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
        reservation_form = ReservationForm(
            request.POST
        )
        reservation_form.instance.listing = current_listing
        reservation_form.instance.user = request.user

        # if form valid - save it and return to post page
        if reservation_form.is_valid():
            reservation_form.save()
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


class UpdateReservation(View):
    """
    Performs operations with single reservation object defined by its public ID
    """
    ACTION = ""

    def get(self, request: HttpRequest, public_id: str) -> HttpResponse:
        """
        Manages operations with selected reservation object
        :param request:
        :param public_id:
        :return:
        """

        try:
            reservation = Reservation.objects.get(
                        id=settings.FF3_CIPHER.decrypt(public_id)
                )
        except Reservation.DoesNotExist:
            raise Http404

        if not reservation.user == self.request.user:
            return HttpResponseForbidden()

        if self.ACTION == "submit":
            reservation.status, _ = ReservationStatus.objects.get_or_create(
                name="Pending"
            )
        elif self.ACTION == "approve":
            reservation.status, _ = ReservationStatus.objects.get_or_create(
                name="Approved"
            )
        elif self.ACTION == "cancel":
            reservation.status, _ = ReservationStatus.objects.get_or_create(
                name="Cancelled"
            )

        reservation.save()

        return redirect("user_display_profile")


class SubmitReservation(UpdateReservation):
    """
    Performs operations with single reservation object defined by its public ID
    """
    ACTION = "submit"


class ApproveReservation(UpdateReservation):
    """
    Performs operations with single reservation object defined by its public ID
    """
    ACTION = "approve"


class CancelReservation(UpdateReservation):
    """
    Performs operations with single reservation object defined by its public ID
    """
    ACTION = "cancel"
