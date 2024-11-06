from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Articles(models.Model):
    """Статья"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=250)
    text = models.TextField(blank=False)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tags', blank=True)
    image = models.ImageField(upload_to='articles/%Y%m%d/', blank=True)
    date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0, blank=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['date']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article', kwargs={'art_pk': self.pk})


class Comments(models.Model):
    """Комментарии о статье"""
    article = models.ForeignKey('Articles', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Categories(models.Model):
    """Категории статей"""
    title = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_pk': self.pk})


class Tags(models.Model):
    """Теги для статей"""
    title = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title
    

class ArticleRating(models.Model):
    """Список всех кому понравилась статья. Одна запись = один лайк"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Оценка статьи'
        verbose_name_plural = 'Оценки статьи'

    def __str__(self):
        return self.user.username
    

class CommentRating(models.Model):
    """Список всех кому понравился комментарий. Одна запись = один лайк"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Оценка комментария'
        verbose_name_plural = 'Оценки комментария'

    def __str__(self):
        return self.user.username