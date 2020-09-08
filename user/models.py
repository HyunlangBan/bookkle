from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=254, nullable = False)
    nickname = models.CharField(max_length=50, nullable = False)
    password = models.CharField(max_length=300, nullable = False)
    follow = models.ManyToManyField('self', symmetrical = False, through = 'Following', related_name='followed')

    class Meta:
        db_table = 'users'


class Following(models.Model):
    follow_from = models.ForeignKey('User', on_delete = models.CASCADE, null = True, related_name = 'following')
    follow_to = models.ForeignKey('User', on_delete = models.CASCADE, null = True, related_name = 'follower')

    class Meta:
        db_table = 'following'
    
