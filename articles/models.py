from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxLengthValidator, MinLengthValidator


class Articles(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=250)
    text = models.TextField(blank=False)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tags', blank=True)
    image = models.ImageField(upload_to='articles/%Y%m%d/', blank=True)
    date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article', kwargs={'art_pk': self.pk})


class Comments(models.Model):
    article = models.ForeignKey('Articles', on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text


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
    

class ArticleRating(models.Model):
    grade = models.IntegerField(default=0, validators=[MaxLengthValidator(1), MinLengthValidator(-1)])
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.grade)
      

class CommentRating(models.Model):
    grade = models.IntegerField(default=0, validators=[MaxLengthValidator(1), MinLengthValidator(-1)])
    comment = models.ForeignKey('Comments', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.grade)
