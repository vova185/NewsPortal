from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.posts.aggregate(pr=Coalesce(Sum('rating'), 0)).get('pr')
        comments_rating = self.user.comments.aggregate(cr=Coalesce(Sum('rating'), 0)).get('cr')
        posts_comments_rating = self.posts.aggregate(pcr=Coalesce(Sum('comment__rating'), 0)).get('pcr')
        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()

class Category(models.Model):
    sport = 'SP'
    culture = 'CUL'
    politics = 'POL'
    education = 'ED'
    nature = 'NAT'
    employment = 'EMP'
    rest = 'RES'
    CATEGORIES = [
        (sport, 'спорт'),
        (culture, 'культура'),
        (politics, 'политика'),
        (education, 'образование'),
        (nature, 'природа'),
        (employment, 'трудоустройство'),
        (rest, 'отдых')
    ]
    all_category = models.CharField(max_length=3, choices=CATEGORIES, default=rest, unique=True)

class Post(models.Model):
    article = 'AR'
    news = 'NS'

    CHOICES = [
        (article, 'Статья'),
        (news, 'Новости')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    genre = models.CharField(max_length=2, choices=CHOICES, default=news)
    time_create = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 255)
    content = models.TextField(max_length = 100000)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        small_content = self.content[:124] + '...'
        return small_content

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.CharField(max_length = 300)
    time_comment = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
