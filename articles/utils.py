from .models import *


class BaseLike:
    """Базовый класс для создания лайков"""
    model = None

    def __init__(self, request, pk):
        self.request = request
        self.pk = pk
        self.get_model_object()

    def get_model_object(self):
        self.model_object = self.model.objects.get(pk=self.pk)
        self.get_like()
    
    def get_like(self):
        pass


class ArticleLike(BaseLike):
    model = Articles

    def get_like(self):
        try:
            ArticleRating.objects.get(user=self.request.user, article=self.model_object)
            self.delete_like()
        except:
            self.create_like()
    
    def create_like(self):
        ArticleRating.objects.create(user=self.request.user, article=self.model_object)

    def delete_like(self):
        ArticleRating.objects.get(user=self.request.user, article=self.model_object).delete()


class CommentLike(BaseLike):
    model = Comments

    def get_like(self):
        try:
            CommentRating.objects.get(user=self.request.user, comment=self.model_object)
            self.delete_like()
        except:
            self.create_like()
    
    def create_like(self, ):
        CommentRating.objects.create(user=self.request.user, comment=self.model_object)

    def delete_like(self):
        CommentRating.objects.get(user=self.request.user, comment=self.model_object).delete()

