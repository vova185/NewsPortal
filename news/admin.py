from django.contrib import admin
from .models import Post, Category


def upper_title(modeladmin, request, queryset):
    for obj in queryset:
        obj.title = obj.title.upper()
        obj.save()
upper_title.short_description = 'Редактировать заголовки прописными буквами'

class PostAdmin(admin.ModelAdmin):

    list_display = ('id', 'time_create', 'genre', 'category', 'title', 'content', 'author')
    list_filter = ('author', 'categories__all_category', 'title')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'time_create')
    actions = [upper_title]

    def category(self, obj):
        return ", ".join([category.all_category for category in obj.categories.all()])

# Register your models here.
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
