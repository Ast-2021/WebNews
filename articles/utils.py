from django.shortcuts import redirect
from .models import *
from .forms import *

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View



def get_comments(art_pk):
    comments = Comments.objects.filter(article__pk=art_pk)
    complete_comment = []
    for comment in comments:
        comment_rating = CommentRating.objects.filter(comment=comment).count()
        users_valuers = [c.user for c in CommentRating.objects.filter(comment=comment)]
        complete_comment.append({'body': comment, 'rating': comment_rating,
                                 'users_valuers': users_valuers})
    return complete_comment


def get_form_for_create_comments(request, article, art_pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_form = form.save()
            new_form.author = request.user
            new_form.article = article
            new_form.save()
            return redirect('article', art_pk)
    else:
        form = CommentForm()
    return form


def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass
    return wrapper