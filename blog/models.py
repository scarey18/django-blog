from django.db import models
from django.utils import timezone

# Create your models here.
class Article(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField()
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.title