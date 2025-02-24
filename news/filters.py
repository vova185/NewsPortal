from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    date = DateFilter(
        field_name='time_create',
        lookup_expr='gt',
        label='Time create is greater than:',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author__user__username': ['icontains'],
            'categories__all_category': ['icontains']
        }
