
from django.shortcuts import redirect
from .models import *
from .forms import *


def get_comments(art_pk):
    comments = Comments.objects.filter(article__pk=art_pk)
    complete_comment = []
    for comment in comments:
        comment_rating = CommentRating.objects.filter(comment=comment).count()
        complete_comment.append({'body': comment, 'rating': comment_rating})
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