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
    path('user_page', views.user_page, name='user_page'),
    path('positive_rating_of_the_comment/<int:pk>', views.positive_rating_of_the_comment, name='positive_rating_of_the_comment'),
    path('negative_rating_of_comment/<int:pk>', views.negative_rating_of_comment, name='negative_rating_of_comment'),
    path('positive_rating_of_the_article/<int:pk>', views.positive_rating_of_the_article, name='positive_rating_of_the_article'),
    path('negative_rating_of_article/<int:pk>', views.negative_rating_of_article, name='negative_rating_of_article' )
]
