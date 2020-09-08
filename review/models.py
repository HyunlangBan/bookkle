from django.db import models
from user.models import User

class Review(models.Model):
    title = models.CharField(max_length = 100)
    content = models.CharField(max_length = 800)
    quote = models.CharField(max_length = 200)
    rating = models.IntegerField()
    book = models.ForeignKey('Book', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

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
    image = models.URLField()

    class Meta:
        db_table = 'books'
    
    
