from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('category/<int:cat_pk>', views.category_view, name='category'),
    path('article/<int:art_pk>', views.article_page, name='article'),
    path('create_article/', views.create_article, name='create_article'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('edit/<int:pk>', views.ArticleUpdateView.as_view(), name='edit'),
    path('delete/<int:art_pk>', views.delete_article, name='delete'),
]
