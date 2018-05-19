from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse

from .models import Article

def custom_filter():
	return Article.objects.filter(pub_date__lte=timezone.now())

class IndexView(ListView):
	template_name = 'blog/index.html'
	context_object_name = 'article_list'

	def get_queryset(self):
		return custom_filter().order_by('-pub_date')

class DetailView(DetailView):
	template_name = 'blog/detail.html'
	model = Article

	def get_queryset(self):
		return custom_filter()

class CreateView(CreateView):
	template_name = 'blog/create.html'
	model = Article
	fields = ['title', 'body']

	def form_valid(self, form):
		pub_date = timezone.now()
		form.instance.pub_date = pub_date
		return super(CreateView, self).form_valid(form)

	def get_success_url(self):
		return reverse('blog:detail', args=(self.object.pk,))