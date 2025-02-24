from django.shortcuts import render, get_object_or_404, redirect

from django.urls import path
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import *
from .filters import PostFilter
from .forms import PostForm
import datetime
from django.views import View

class NewsList(ListView):
    model = Post
    ordering = '-time_create'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 10

class CategoryListView(NewsList):
    model = Post
    template_name = 'flatpages/category.html'
    context_object_name = 'category_news_list'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category).order_by('-time_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

def subscribers(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return redirect(request.META['HTTP_REFERER'])

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
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        today = datetime.date.today()
        post_limit = Post.objects.filter(author=post.author, time_create__date=today).count()

        if self.request.path == 'articles/create/':
            post.genre = 'AR'

        if post_limit >= 3:
            return render(self.request, 'flatpages/post_limit.html', {'author': post.author})
        post.save()
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
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

