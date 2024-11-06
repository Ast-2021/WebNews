from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60)(views.ArticlesHome.as_view()), name='home'),
    path('category/<int:cat_pk>', cache_page(60)(views.CategoryView.as_view()), name='category'),
    path('article/<int:art_pk>', views.article_page, name='article'),
    path('create_article/', views.CreateArticle.as_view(), name='create_article'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('edit/<int:pk>', views.ArticleUpdateView.as_view(), name='edit'),
    path('delete_article/<int:art_pk>', views.delete_article, name='delete_article'),
    path('delete_comment/<int:com_pk>', views.delete_comment, name='delete_comment'),
    path('user_page', views.user_page, name='user_page'),
    path('article_rating/<int:pk>', views.article_rating, name='article_rating'),
    path('comment_rating/<int:pk>', views.comment_rating, name='comment_rating'),
]