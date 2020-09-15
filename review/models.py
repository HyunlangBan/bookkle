from django.db import models
from user.models import User

class Review(models.Model):
    title = models.CharField(max_length = 100)
    content = models.CharField(max_length = 800)
    quote = models.CharField(max_length = 100, null = True)
    rating = models.IntegerField()
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    book = models.ForeignKey('Book', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    liker = models.ManyToManyField(User, blank = True, through ='like', related_name='review_like')

    class Meta:
        db_table = 'reviews'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'like')
    review = models.ForeignKey('Review', on_delete = models.CASCADE, related_name = 'like')

    class Meta:
        db_table = 'likes'
        unique_together = ('user', 'review')

class Book(models.Model):
    title = models.CharField(max_length = 100)
    author = models.CharField(max_length = 50)
    image = models.URLField(null = True)

    class Meta:
        db_table = 'books'
    

