from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from .models import *

def custom_filter():
	return Article.objects.filter(pub_date__lte=timezone.now())

class IndexView(ListView):
	template_name = 'blog/index.html'
	context_object_name = 'article_list'

	def get_queryset(self):
		return custom_filter().order_by('-pub_date')

class TagListView(ListView):
	template_name = 'blog/tag_list.html'
	context_object_name = 'tag_list'

	def get_queryset(self):
		return Tag.objects.all()

class DetailView(DetailView):
	template_name = 'blog/detail.html'
	model = Article

	def get_queryset(self):
		return custom_filter()

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

def tag_view(request, pk):
	tag = get_object_or_404(Tag, pk=pk)
	context = {
		'tag': tag,
	}
	return render(request, 'blog/tag.html', context)

def create_view(request):
	return render(request, 'blog/create.html')

def edit_view(request, pk):
	return render(request, 'blog/create.html', {'article': Article.objects.get(pk=pk),})

def create_article(request):
	title = request.POST['title']
	body = request.POST['body']
	tags = request.POST['tags'].split(', ')

	article = Article.objects.create(title=title, body=body, pub_date=timezone.now())
	article.save()
	for t in tags:
		tag = None
		if t in [n.name for n in Tag.objects.all()]:
			tag = Tag.objects.get(name=t)
		else:
			tag = Tag.objects.create(name=t)
			tag.save()
		Tagging.objects.create(tag=tag, article=article).save()

	return HttpResponseRedirect(reverse('blog:detail', args=(article.pk,)))

def edit_article(request, pk):
	title = request.POST['title']
	body = request.POST['body']
	tags = request.POST['tags'].split(', ')
	article = Article.objects.get(pk=pk)
	taggings = article.tag_list().split(', ')
	full_tag_list = [t.name for t in Tag.objects.all()]

	article.title = title
	article.body = body
	article.save()

	for t in tags:
		if t not in full_tag_list:
			tag = Tag.objects.create(name=t)
			tag.save()
			Tagging.objects.create(tag=tag, article=article).save()
		elif t not in taggings:
			tag = Tag.objects.get(name=t)
			Tagging.objects.create(tag=tag, article=article).save()

	for t in taggings:
		if t not in tags:
			tag = Tag.objects.get(name=t)
			tagging = Tagging.objects.get(tag=tag, article=article)
			tagging.delete()

	return HttpResponseRedirect(reverse('blog:detail', args=(article.pk,)))
