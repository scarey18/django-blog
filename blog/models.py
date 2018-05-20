from django.db import models
from django.utils import timezone

# Create your models here.
class Article(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField()
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.title

class Comment(models.Model):
	author = models.CharField(max_length=30)
	body = models.TextField()
	article = models.ForeignKey(Article, on_delete=models.CASCADE)
	posted_at = models.DateTimeField(default=timezone.now())

	def __str__(self):
		return self.author
