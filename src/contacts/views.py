from django.http import (
    HttpRequest, HttpResponse, Http404,
    HttpResponseRedirect
)
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from .forms import ContactForm
from .models import Company


class Contacts(View):
    """
    Company info view with contact form
    """

    model = Company
    template_name = "contacts/contacts.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Displays selected post detail in common with comment form
        :param request:
        :return:
        """

        try:
            context: dict = {
                "company": self.model.objects.all()[0],
                "contact_form": ContactForm()
            }
            return render(
                request,
                self.template_name,
                context
            )
        except Company.DoesNotExist:
            raise Http404(
                "The company info is not available"
            )

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Processing new contact form message
        :param self:
        :param request:
        :param slug
        :return:
        """

        contact_form = ContactForm(request.POST)

        # if form valid - save it and return to post page
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            contact.is_processed = False
            contact_form.save()
            return HttpResponseRedirect(
                reverse(
                    "contacts:company_info"
                )
            )

        # if form isn't valid - reload post page with form errors included
        context = {
            "company": self.model.objects.all()[0],
            "contact_form": contact_form

        }
        return render(
            request,
            self.template_name,
            context
        )
