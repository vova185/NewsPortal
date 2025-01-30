from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'

class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/publication.html'
    context_object_name = 'publication'
    pk_url_kwarg = 'id'

