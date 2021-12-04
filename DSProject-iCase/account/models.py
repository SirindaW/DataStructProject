from typing import DefaultDict
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, UserManager

# Create your models here.

# create a new user
# create a superuser

class MyAccountManager(BaseUserManager):
    def create_user(self,email,password=None ):
        if not email:
            raise ValueError("User must have an email address")
        # if not username:
        #     raise ValueError("User must have a username")
        
        user = self.model(
            # for handling capitalized email characters
            email = self.normalize_email(email),
            # username = username,
        )
        user.set_password(password) 
        user.save(using=self._db)
        return user
        
    def create_superuser(self,email,password):
        user = self.create_user (
            email = self.normalize_email(email),
            # username = username,
            password = password,
            
        )
        user.is_admin = True
        user.is_staff= True
        user.is_superuser= True

        user.set_password(password) 
        user.save(using=self._db)
        return user




def get_profile_image_filepath(self):
    return f'profile_images/{self.pk}/{"profile_image.png"}'


class Account(AbstractBaseUser):
    
    email = models.EmailField(verbose_name="email",max_length=60,unique=True)
    # username = models.CharField(max_length = 30,unique = True)
    first_name = models.CharField(max_length=100,blank=False,null=False,default='')
    last_name = models.CharField(max_length=100,blank=False,null=False,default='')
    date_joined = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login',auto_now=True)

    # Already included in AbstractBaseUser class, so we need to overwrite these in order to use this model to extend our user model
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)

    profile_image = models.ImageField(max_length=255,upload_to=get_profile_image_filepath,null=True,blank=True)
    hide_email = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

    # Override
    def has_perm(self,perm ,obj = None):
        return self.is_admin

    # Override
    def has_module_perms(self,app_label):
        return True
    

