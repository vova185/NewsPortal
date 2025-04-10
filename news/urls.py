from django.urls import path
from .views import (
    NewsList, NewsDetail, subscribers, FilterList, PostCreate, PostUpdate, PostDelete, CategoryListView, IndexView
)

urlpatterns = [
path('news/', NewsList.as_view(), name='post_list'),
path('news/<int:id>', NewsDetail.as_view(), name='post_detail'),
path('news/search/', FilterList.as_view()),
path('news/create/', PostCreate.as_view(), name='news_create'),
path('articles/create/', PostCreate.as_view(), name='articles_create'),
path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_update'),
path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
path('categories/<int:pk>/subscribe', subscribers, name='subscribe'),
path('', IndexView.as_view())
]

