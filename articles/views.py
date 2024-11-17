from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.db.models import Count

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


class CategoryView(ArticlesHome):
    """Статьи с определенной категорией"""

    def get_queryset(self):
        return Articles.objects.filter(category__pk=self.kwargs['pk'])


class ArticlePage(DetailView):
    model = Articles
    template_name = 'articles/article_page.html'
    context_object_name = 'article'

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            new_form = form.save()
            new_form.author = request.user
            new_form.article = self.get_object()
            new_form.save()
            logger.info(f'User id({request.user.id}) posted a comment id({new_form.pk})')
            return redirect('article', self.get_object().pk)
        
    def get_queryset(self):
        queryset = Articles.objects.annotate(rating=Count('articleratings'))
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        article_id = self.kwargs.get('pk')
        return get_object_or_404(queryset, pk=article_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        context['categories'] = Categories.objects.all()
        context['comments'] = Comments.get_comment_queryset(article.id)
        context['article'] = Articles.get_article(article)
        return context


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
    logout(request)
    return redirect('login')


class DeleteArticle(LoginRequiredMixin, DeleteView):
    model = Articles
    template_name = 'articles/delete_article.html'
    success_url = reverse_lazy('home')


class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comments
    template_name = 'articles/delete.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        article_id = str(self.object.article.id)
        return reverse('article', kwargs={'pk': article_id})


class UserPage(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'articles/user_page.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Articles.objects.filter(author=self.request.user)
        context['comments'] = Comments.objects.filter(author=self.request.user)
        return context


@login_required(login_url='login')
def article_rating(request, pk):
    ArticleLike(request, pk)
    return redirect('article', pk)


@login_required(login_url='login')
def comment_rating(request, pk):
    comment_rat = CommentLike(request, pk)
    return redirect('article', comment_rat.model_object.article.pk)
    