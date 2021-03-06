from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser): 
    username = None
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    department = models.CharField(null=True,max_length=255,default='' )
    language_learnt = models.CharField(max_length=100,default='',null=True,blank=True)
    pic = models.TextField(blank=True,null=True,default='https://www.pinclipart.com/picdir/middle/8-82428_profile-clipart-generic-user-gender-neutral-head-icon.png')
    self_introduction = models.TextField(default='',null=True,blank=True)

    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []
    objects = UserManager()
    

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name





    
    
   

