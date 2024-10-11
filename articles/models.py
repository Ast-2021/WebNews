from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Articles(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    text = models.TextField(blank=False)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tags')
    image = models.ImageField(upload_to='articles/%Y%m%d/', blank=True)
    date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article', kwargs={'art_pk': self.pk})


class Comments(models.Model):
    article = models.ForeignKey('Articles', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)


class Categories(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_pk': self.pk})


class Tags(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title