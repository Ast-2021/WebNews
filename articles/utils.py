from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

import logging

logger = logging.getLogger('main')


def get_comments(art_pk):
    """Возвращает комментарии с их рейтингом (кол-вом лайков)"""
    comments = Comments.objects.filter(article__pk=art_pk)
    complete_comment = []
    for comment in comments:
        comment_rating = CommentRating.objects.filter(comment=comment).count()
        users_valuers = [c.user for c in CommentRating.objects.filter(comment=comment)]
        complete_comment.append({'body': comment, 'rating': comment_rating,
                                 'users_valuers': users_valuers})
    return complete_comment


def get_form_for_create_comments(request, article, art_pk):
    """Создание комментарий"""
    user_with_authorization = str(request.user) != 'AnonymousUser'
    if request.method == 'POST' and user_with_authorization:
        form = CommentForm(request.POST)
        if form.is_valid():
            new_form = form.save()
            new_form.author = request.user
            new_form.article = article
            new_form.save()

            logger.info(f'User id({request.user.id}) posted a comment id({new_form.pk})')
            
            return redirect('article', art_pk)
    else:
        form = CommentForm()
    return form
