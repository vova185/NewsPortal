from django.shortcuts import render

from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post
from .filters import PostFilter
from .forms import PostForm

class NewsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 10

class FilterList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'flatpages/filter.html'
    context_object_name = 'filter'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/publication.html'
    context_object_name = 'publication'
    pk_url_kwarg = 'id'

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == 'articles/create/':
            post.genre = 'AR'
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    def get_context_data(self, **kwargs):
        post = self.get_object()
        context = super().get_context_data(**kwargs)
        context['valid_genre'] = (self.request.path == f'/articles/{post.id}/edit/' and post.genre == Post.article) or \
                                 (self.request.path == f'/news/{post.id}/edit/' and post.genre == Post.news)
        return context

class PostDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        post = self.get_object()
        context = super().get_context_data(**kwargs)
        context['valid_genre'] = (self.request.path == f'/articles/{post.id}/delete/' and post.genre == Post.article) or \
                                 (self.request.path == f'/news/{post.id}/delete/' and post.genre == Post.news)
        return context

