from django.shortcuts import render
from .models import *


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
    categories = Categories.objects.all()
    context = {'categories': categories, 'article': article}
    return render(request, 'articles/article_page.html', context=context)