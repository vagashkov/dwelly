from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic import View

from core.models import BaseModel

from .forms import CommentForm
from .models import Post


class Posts(ListView):
    """
    All posts view
    """

    model = Post
    ordering = "-{}".format(BaseModel.Field.created_at)
    template_name = "blog/index.html"
    context_object_name = "posts"


class PostDetails(View):
    """
    Single post details view with comments and commenting form
    """

    model = Post
    template_name = "blog/post_details.html"

    def get(self, request, slug):
        """
        Displays selected post detail in common with comment form
        :param request:
        :param slug:
        :return:
        """

        try:
            context: dict = {
                "post": self.model.objects.get(
                    slug=slug
                ),
                "comment_form": CommentForm()
            }
            return render(
                request,
                self.template_name,
                context
            )
        except Post.DoesNotExist:
            raise Http404(
                "The post doesn't exist"
            )

    def post(self, request, slug):
        """
        Processing new post comment
        :param self:
        :param request:
        :param slug
        :return:
        """

        current_post = self.model.objects.get(slug=slug)
        comment_form = CommentForm(request.POST)

        # if form valid - save it and return to post page
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = current_post
            comment.save()
            return HttpResponseRedirect(
                reverse(
                    "post_details",
                    args=[
                        slug
                    ]
                )
            )

        # if form isn't valid - reload post page with form errors included
        context = {
            "post": current_post,
            "comment_form": comment_form
        }
        return render(
            request,
            self.template_name,
            context
        )
