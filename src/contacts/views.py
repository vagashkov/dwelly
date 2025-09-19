from django.http import (
    HttpRequest, HttpResponse, Http404
)
from django.shortcuts import render
from django.views.generic import View

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
                # "comment_form": CommentForm()
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
