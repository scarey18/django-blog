from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Article
from datetime import timedelta

# Create your tests here.
def create_test_article(article_id='1', days=0, hours=0, minutes=0, seconds=0):
    """
    Creates an article with the specified pub_date for testing purposes.
    """
    time = timezone.now() + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return Article.objects.create(title='Test article %s' % article_id, body='This is test article %s' % article_id, pub_date=time)

class ArticleIndexViewTests(TestCase):
    def test_no_articles(self):
        '''
        If there are no published articles, index view should display "No articles are available."
        '''
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No articles are available.')
        self.assertQuerysetEqual(response.context['article_list'], [])

    def test_past_articles(self):
        '''
        Index view should display a list of articles published in the past
        '''
        create_test_article(days=-30)
        create_test_article('2', seconds=-1)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context['article_list'], ['<Article: Test article 2>', '<Article: Test article 1>'])

    def test_future_articles(self):
        '''
        If there are only future articles, index view should display "no articles are available."
        '''
        create_test_article(seconds=1)
        create_test_article('2', days=40)
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No articles are available.')
        self.assertQuerysetEqual(response.context['article_list'], [])

    def test_past_and_future_articles(self):
        '''
        Index view should only display past articles.
        '''
        create_test_article(days=-5)
        create_test_article('2', days=5)
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context['article_list'], ['<Article: Test article 1>'])

class ArticleDetailViewTests(TestCase):
    def test_future_article(self):
        '''
        The detail view of an article with a pub_date in the future returns a 404 not found.
        '''
        future_article = create_test_article(days=30)
        url = reverse('blog:detail', args=(future_article.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    def test_past_article(self):
        '''
        The detail view of an article with a pub_date in the past displays the article title and body.
        '''
        past_article = create_test_article(seconds=-1)
        url = reverse('blog:detail', args=(past_article.pk,))
        response = self.client.get(url)
        self.assertContains(response, past_article.title)
        self.assertContains(response, past_article.body)