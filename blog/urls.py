from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('articles/<int:pk>/', views.DetailView.as_view(), name='detail'),
	path('create/', views.create_view, name='create'),
	path('articles/<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
	path('articles/<int:pk>/edit/', views.edit_view, name='edit'),
	path('<int:pk>/comment/', views.post_comment, name='post_comment'),
	path('tags/<int:pk>/', views.tag_view, name='tag'),
	path('create_article/', views.create_article, name='create_article'),
	path('articles/<int:pk>/edit_article/', views.edit_article, name='edit_article'),
	path('tags/', views.TagListView.as_view(), name='tag_list')
]