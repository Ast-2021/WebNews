from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import *
from django.views.generic.edit import CreateView, UpdateView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
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
    categories = Categories.objects.all()
    context = {'categories': categories, 'article': article}
    return render(request, 'articles/article_page.html', context=context)


@login_required()
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