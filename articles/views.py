from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page

from .utils import *
from .forms import *
from .models import *

import logging


logger = logging.getLogger('main')


class ArticlesHome(ListView):
    """Главная страница"""
    model = Articles
    template_name = 'articles/index.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context


class CategoryView(ListView):
    """Статьи с определенной категорией"""
    model = Articles
    template_name = 'articles/index.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context
    
    def get_queryset(self):
        return Articles.objects.filter(category__pk=self.kwargs['cat_pk'])


@cache_page(60)
def article_page(request, art_pk):
    """Страница статьи"""
    article = Articles.objects.get(pk=art_pk)
    article_rating = ArticleRating.objects.filter(article=article).count()
    categories = Categories.objects.all()

    article_valuers = [a.user for a in ArticleRating.objects.filter(article=article)]

    form = get_form_for_create_comments(request, article, art_pk)
    comments = get_comments(art_pk)

    context = {'categories': categories, 'article': article, 'form': form, 
               'article_rating': article_rating, 'comments': comments, 
               'article_valuers': article_valuers}
    return render(request, 'articles/article_page.html', context=context)


class CreateArticle(LoginRequiredMixin, CreateView):
    """Создание статьи"""
    login_url = 'login'
    
    form_class = ArticleForm
    template_name = 'articles/create_article.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    """Редактирование статьи"""
    model = Articles
    fields = ['title', 'text', 'image', 'category', 'tags']
    template_name = 'articles/create_article.html'
    success_url = reverse_lazy('home')


class RegisterUser(CreateView):
    """Регистарция пользователя"""
    form_class = RegisterUserForm
    template_name = 'articles/register.html'
    
    def get_success_url(self):
        return reverse_lazy('home')


class LoginUser(LoginView):
    """Авторизация пользователя"""
    form_class = LoginUserForm
    template_name = 'articles/login.html'
    success_url = reverse_lazy('home')


def logout_user(request):
    """Выход из аккаунта"""
    logout(request)
    return redirect('login')


def delete_article(request, art_pk):
    """Удаление статьи"""
    Articles.objects.get(pk=art_pk).delete()

    logger.info(f'User id({request.user.id}) deleted article id({art_pk})')

    return redirect('home')


def delete_comment(request, com_pk):
    """Удаление комментария"""
    article_pk = Comments.objects.get(pk=com_pk).article.pk
    Comments.objects.get(pk=com_pk).delete()

    logger.info(f'User id({request.user.id} deleted comment id({com_pk}))')

    return redirect('article', article_pk)


def user_page(request):
    """Страница пользователя с его статьями, и комментариями"""
    user = User.objects.get(username=request.user.username)
    articles = Articles.objects.filter(author=user)
    comments = Comments.objects.filter(author=user)
    
    context = {'articles': articles, 'user': user, 'comments': comments}
    return render(request, 'articles/user_page.html', context=context)


@login_required(redirect_field_name='login')
def article_rating(request, pk):
    """Поставить лайк статье, либо удалить его если он уже стоит"""
    article = Articles.objects.get(pk=pk)
    try:
        if ArticleRating.objects.get(user=request.user, article=article):
            ArticleRating.objects.get(user=request.user, article=article).delete()

            logger.info(f'User id({request.user.id}) removed the like from article id({article.pk})')
    except:
        ArticleRating.objects.create(user=request.user, article=article)

        logger.info(f'User id({request.user.id}) liked article id({article.pk})')

    return redirect('article', article.pk)


@login_required(redirect_field_name='login')
def comment_rating(request, pk):
    """Поставить лайк комментарию, либо удалить его если он уже стоит"""
    comment = Comments.objects.get(pk=pk)
    try:
        if CommentRating.objects.get(user=request.user, comment=comment):
            CommentRating.objects.get(user=request.user, comment=comment).delete()

            logger.info(f'User id({request.user.id}) removed the like from comment id({comment.pk})')
    except:
        CommentRating.objects.create(user=request.user, comment=comment)
        
        logger.info(f'User id({request.user.id}) liked comment id({comment.pk})')

    return redirect('article', comment.article.pk)
