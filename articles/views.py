from functools import reduce
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import *
from django.views.generic.edit import CreateView, UpdateView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout


def index(request):
    categories = Categories.objects.all()
    articles = Articles.objects.all()
    context = {'categories': categories, 'articles': articles}
    return render(request, 'articles/index.html', context=context)


def category_view(request, cat_pk):
    category = Categories.objects.get(pk=cat_pk)
    categories = Categories.objects.all()
    articles = Articles.objects.filter(category=category)
    context = {'categories': categories, 'articles': articles}
    return render(request, 'articles/index.html', context=context)
    

def article_page(request, art_pk):
    article = Articles.objects.get(pk=art_pk)
    comments = Comments.objects.filter(article__pk=art_pk)
    article_rating = ArticleRating.objects.count()
    complete_comment = []
    for comment in comments:
        comment_rating = CommentRating.objects.filter(comment=comment).count()
        complete_comment.append({'body': comment, 'rating': comment_rating})

    categories = Categories.objects.all()

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

    context = {'categories': categories, 'article': article, 'form': form, 
               'article_rating': article_rating, 'comments': complete_comment}
    return render(request, 'articles/article_page.html', context=context)


@login_required(login_url='login')
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save()
            newform.author = request.user
            newform.save()
            return redirect('home')
    else:
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'articles/create_article.html', context=context)
        

class ArticleUpdateView(UpdateView):
    model = Articles
    fields = ['title', 'text', 'category', 'tags']
    template_name = 'articles/create_article.html'
    success_url = reverse_lazy('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'articles/register.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'articles/login.html'

    def get_success_url(self):
        return reverse_lazy('home')
    

def logout_user(request):
    logout(request)
    return redirect('login')


def delete_article(request, art_pk):
    Articles.objects.get(pk=art_pk).delete()
    return redirect('home')


def user_page(request):
    articles = Articles.objects.filter(author=request.user)
    user = User.objects.get(username=request.user.username)
    comments = Comments.objects.filter(author=user)
    context = {'articles': articles, 'user': user, 'comments': comments}
    return render(request, 'articles/user_page.html', context=context)


def article_rating(request, pk):
    article = Articles.objects.get(pk=pk)
    try:
        if ArticleRating.objects.get(user=request.user, article=article):
            ArticleRating.objects.get(user=request.user, article=article).delete()

    except:
        ArticleRating.objects.create(user=request.user, article=article)
    return redirect('article', article.pk)


def comment_rating(request, pk):
    comment = Comments.objects.get(pk=pk)
    try:
        if CommentRating.objects.get(user=request.user, comment=comment):
            CommentRating.objects.get(user=request.user, comment=comment).delete()
    except:
        CommentRating.objects.create(user=request.user, comment=comment)
    return redirect('article', comment.article.pk)