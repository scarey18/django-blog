from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from .models import Article, Comment

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

class DeleteView(DeleteView):
	template_name = 'blog/delete.html'
	model = Article
	success_url = reverse_lazy('blog:index')

	def get_queryset(self):
		return custom_filter()

class EditView(UpdateView):
	template_name = 'blog/create.html'
	model = Article
	fields = ['title', 'body']

	def get_success_url(self):
		return reverse('blog:detail', args=(self.object.pk,))

	def get_queryset(self):
		return custom_filter()

def post_comment(request, pk):
	author = request.POST['author']
	body = request.POST['body']
	article = get_object_or_404(Article, pk=pk)

	if author == '' or body == '':
		context = {
		'article': article,
		'error_message': "Please fill out both fields",
		'author': author,
		'body': body,
		}
		return render(request, 'blog/detail.html', context)

	comment = Comment.objects.create(author=author, body=body, article=article)
	comment.save()

	return HttpResponseRedirect(reverse('blog:detail', args=(pk,)))
