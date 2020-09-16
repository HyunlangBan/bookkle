from django.db import models
from user.models import User

class Review(models.Model):
    title = models.CharField(max_length = 100)
    content = models.CharField(max_length = 800)
    quote = models.CharField(max_length = 100, null = True)
    rating = models.IntegerField()
    recommend_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    book = models.ForeignKey('Book', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    recommender = models.ManyToManyField(User, blank = True, through ='recommend', related_name='review_recommend')

    class Meta:
        db_table = 'reviews'

class Recommend(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'recommend')
    review = models.ForeignKey('Review', on_delete = models.CASCADE, related_name = 'recommend')

    class Meta:
        db_table = 'recommends'
        unique_together = ('user', 'review')

class Book(models.Model):
    title = models.CharField(max_length = 100)
    author = models.CharField(max_length = 50)
    image = models.URLField(null = True)

    class Meta:
        db_table = 'books'
    

