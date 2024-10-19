from django.test import TestCase, Client
from django.urls import reverse

from .models import Articles, Categories, Comments, User, CommentRating, ArticleRating


class TestViews(TestCase):
    """Тестирование классов и функций модуля views.py"""

    def setUp(self):
        self.client = Client()
        self.category_1 = Categories.objects.create(title='test_category')
        self.category_2 = Categories.objects.create(title='cool_category')
        self.article_1 = Articles.objects.create(title='test_article', text='test_text', category=self.category_1)
        self.article_2 = Articles.objects.create(title='cool_article', text='cool_text', category=self.category_2)
        self.user = User.objects.create_user(username='username', password='password')
        self.comment = Comments.objects.create(article=self.article_1, author=self.user, text='test_comment')

        self.client.login(username='username', password='password')

        self.url_article_page = reverse('article', args=[self.article_1.pk])
        self.url_category = reverse('category', args=[self.category_1.pk])
        self.url_create_article = reverse('create_article')
        self.url_update_article = reverse('edit', args=[self.article_1.pk])
        self.url_register_user = reverse('register')
        self.url_login_user = reverse('login')
        self.url_delete_article = reverse('delete', args=[self.article_1.pk])
        self.url_user_page = reverse('user_page')
        self.url_positive_rating_of_the_comment = reverse('positive_rating_of_the_comment', args=[self.comment.pk])
        self.url_negative_rating_of_comment = reverse('negative_rating_of_comment', args=[self.comment.pk])
        self.url_positive_rating_of_the_article = reverse('positive_rating_of_the_article', args=[self.article_1.pk])
        self.url_negative_rating_of_article = reverse('negative_rating_of_article', args=[self.article_1.pk])


    def test_index(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('test_article', response.content.decode('utf-8'))
        self.assertIn('cool_article', response.content.decode('utf-8'))
        self.assertTemplateUsed(response, 'articles/index.html')


    def test_category_view(self):
        response = self.client.get(self.url_category)

        self.assertEqual(response.status_code, 200)
        self.assertIn('test_category', response.content.decode('utf-8'))
        self.assertNotIn('cool_article', response.content.decode('utf-8'))

    
    def test_article_page(self):
        response = self.client.get(self.url_article_page)

        self.assertEqual(response.status_code, 200)
        self.assertIn('test_article', response.content.decode('utf-8'))
        self.assertIn('test_comment', response.content.decode('utf-8'))
        self.assertNotIn('Cool article', response.content.decode('utf-8'))

        response_2 = self.client.post(self.url_article_page, {
            'text': 'Cool article'
        })

        self.assertEqual(response_2.status_code, 302)
        self.assertEqual(Comments.objects.count(), 2)
        self.assertEqual(Comments.objects.last().text, 'Cool article')


    def test_create_article(self):
        response = self.client.post(self.url_create_article, {
            'title': 'Моя новая статья',
            'text': 'то содержимое моей статьи',
            'category': self.category_1.pk,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Articles.objects.count(), 3)
        self.assertEqual(Articles.objects.last().title, 'Моя новая статья')

    
    def test_update_article(self):
        response = self.client.post(self.url_update_article, {
            'title': 'Моя уже обновлянная первая статья',
            'text': 'то содержимое моей статьи',
            'category': self.category_1.pk,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Articles.objects.count(), 2)
        self.assertEqual(Articles.objects.first().title, 'Моя уже обновлянная первая статья')


    def test_register_user(self):
        self.client.logout()
        response = self.client.post(self.url_register_user, {
            'username': 'username_2',
            'password1': 'passwordpassword',
            'password2': 'passwordpassword',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().username, 'username_2')

    
    def test_login_user(self):
        self.client.logout()
        response = self.client.post(self.url_login_user, {
            'username': 'username',
            'password': 'password',
        })

        self.assertEqual(response.status_code, 302)


    def test_delete_article(self):
        response = self.client.get(self.url_delete_article)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Articles.objects.count(), 1)
        self.assertNotEqual(Articles.objects.first().title, 'test_article')


    def test_user_page(self):
        response = self.client.get(self.url_user_page)

        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.content.decode('utf-8'))


    def test_positive_rating_of_the_comment(self):
        response = self.client.get(self.url_positive_rating_of_the_comment)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(CommentRating.objects.first().grade, 1)


    def test_negative_rating_of_comment(self):
        response = self.client.get(self.url_negative_rating_of_comment)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(CommentRating.objects.first().grade, -1)

    
    def test_positive_rating_of_the_article(self):
        response = self.client.get(self.url_positive_rating_of_the_article)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ArticleRating.objects.first().grade, 1)

    
    def test_negative_rating_of_article(self):
        response = self.client.get(self.url_negative_rating_of_article)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ArticleRating.objects.first().grade, -1)