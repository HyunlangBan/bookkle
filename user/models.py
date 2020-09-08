from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=254, null = False, unique = True)
    nickname = models.CharField(max_length=50, null = False, unique = True)
    password = models.CharField(max_length=300, null = False)
    follow = models.ManyToManyField('self', symmetrical = False, through = 'Following', related_name='followed')

    class Meta:
        db_table = 'users'


class Following(models.Model):
    follow_from = models.ForeignKey('User', on_delete = models.CASCADE, null = True, related_name = 'following')
    follow_to = models.ForeignKey('User', on_delete = models.CASCADE, null = True, related_name = 'follower')

    class Meta:
        db_table = 'following'
        unique_together = ('follow_from', 'follow_to')
    
