from django.db import models
from user.models import User

class Review(models.Model):
    title = models.CharField(max_length = 100)
    content = models.CharField(max_length = 800)
    quote = models.CharField(max_length = 100, null = True)
    rating = models.IntegerField()
    recommand_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    book = models.ForeignKey('Book', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    recommander = models.ManyToManyField(User, blank = True, through ='Recommand', related_name='review_like')

    class Meta:
        db_table = 'reviews'

class Recommand(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'recommand')
    review = models.ForeignKey('Review', on_delete = models.CASCADE, related_name = 'recommand')

    class Meta:
        db_table = 'recommandations'
        unique_together = ('user', 'review')

class Book(models.Model):
    title = models.CharField(max_length = 100)
    author = models.CharField(max_length = 50)
    image = models.URLField(null = True)

    class Meta:
        db_table = 'books'
    

