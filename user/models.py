from django.db import models 
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class UserManager(BaseUserManager):    
    def create_user(self, email, nickname, password=None, **kwargs):        
        
        if not email :            
            raise ValueError('must have user email')        
        user = self.model(            
            email = self.normalize_email(email),            
            nickname = nickname        
        )        
        user.set_password(password)        
        user.save(using=self._db)        
        return user     

    def create_superuser(self, email, nickname,password ):        
       
        user = self.create_user(            
            email = self.normalize_email(email),            
            nickname = nickname,            
            password=password        
        )        
        user.is_admin = True        
        user.is_superuser = True        
        user.is_staff = True   
        user.save(using=self._db)        
        return user 

class User(AbstractBaseUser,PermissionsMixin):    
    
    objects = UserManager()
    
    email = models.EmailField(        
        max_length=255,        
        unique=True,    
    )    
    nickname = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )     
    follower_count = models.IntegerField(default = 0)
    following = models.ManyToManyField('User', through='Follow', blank=True, related_name='followed')

    is_active = models.BooleanField(default=False)    
    is_admin = models.BooleanField(default=False)    
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)     

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['nickname']



class Follow(models.Model):
    follow_from = models.ForeignKey('User', on_delete = models.CASCADE, null = False, related_name = 'follow_to')
    follow_to = models.ForeignKey('User', on_delete = models.CASCADE, null = False, related_name = 'follow_from')

    class Meta:
        db_table = 'follows'
        unique_together = ('follow_from', 'follow_to')
    
