from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('category/<int:cat_pk>', views.category_view, name='category'),
    path('article/<int:art_pk>', views.article_page, name='article')
]
