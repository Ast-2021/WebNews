from functools import reduce
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import *
from django.views.generic.edit import CreateView, UpdateView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout


def sum_of_all_elements_of_the_iterable_object(iter_obj):
    if len(iter_obj) == 0:
        return 0
    elif len(iter_obj) == 1:
        return iter_obj[0]
    elif len(iter_obj) > 2:
        return iter_obj[0].grade + sum_of_all_elements_of_the_iterable_object(iter_obj[1:])
    else:
        return iter_obj[0].grade + iter_obj[1].grade


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
    categories = Categories.objects.all()
    try:
        user_article_rating = ArticleRating.objects.get(user=request.user).grade
        user_comment_rating = CommentRating.objects.get(user=request.user).grade
    except:
        user_article_rating = 0
        user_comment_rating = 0

    article_rating = sum_of_all_elements_of_the_iterable_object(ArticleRating.objects.filter(article=article))

    full_comments = []
    for comment in comments:
        try:
            comment_rating = sum_of_all_elements_of_the_iterable_object(CommentRating.objects.filter(comment=comment))
        except:
            comment_rating = 99
        full_comments.append({'body_comment': comment, 'comment_rating': comment_rating})

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

    context = {'categories': categories, 'article': article, 'comments': full_comments, 'form': form, 
               'user_comment_rating': user_comment_rating, 'user_article_rating': user_article_rating, 'article_rating': article_rating}
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


def positive_rating_of_the_comment(request, pk):
    comment = Comments.objects.get(pk=pk)
    try:
        CommentRating.objects.create(grade=1, comment=comment, user=request.user)
    except:
        if CommentRating.objects.get(user=request.user, comment=comment).grade != 1:
            com_rat = CommentRating.objects.get(user=request.user, comment=comment)
            com_rat.grade = 1
            com_rat.save()
        else:
            pass
    return redirect('article', comment.article.pk)


def negative_rating_of_comment(request, pk):
    comment = Comments.objects.get(pk=pk)
    try:
        CommentRating.objects.create(grade=-1, comment=comment, user=request.user)
    except:
        if CommentRating.objects.get(user=request.user, comment=comment).grade != -1:
            com_rat = CommentRating.objects.get(user=request.user, comment=comment)
            com_rat.grade = -1
            com_rat.save()
        else:
            pass

    return redirect('article', comment.article.pk)


def positive_rating_of_the_article(request, pk):
    article = Articles.objects.get(pk=pk)
    try:
        ArticleRating.objects.create(grade=1, article=article, user=request.user)
    except:
        if ArticleRating.objects.get(user=request.user, article=article).grade != 1:
            art_rat = ArticleRating.objects.get(user=request.user, article=article)
            art_rat.grade = 1
            art_rat.save()
        else:
            pass

    return redirect('article', article.pk)


def negative_rating_of_article(request, pk):
    article = Articles.objects.get(pk=pk)
    try:
        ArticleRating.objects.create(grade=-1, article=article, user=request.user)
    except:
        if ArticleRating.objects.get(user=request.user, article=article).grade != -1:
            art_rat = ArticleRating.objects.get(user=request.user, article=article)
            art_rat.grade = -1
            art_rat.save()
        else:
            pass

    return redirect('article', article.pk)