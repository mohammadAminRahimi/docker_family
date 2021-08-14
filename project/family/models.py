from project.settings import AUTH_USER_MODEL
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields import CharField
from django.db.models.signals import post_save

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


from django.dispatch import receiver
from rest_framework.authtoken.models import Token




class family(models.Model):
    family_id = models.CharField(max_length=30, primary_key=True)
    member_count = models.IntegerField()


class package(models.Model):
    type = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')], primary_key=True)
    description = models.CharField(max_length=300, null=True)


class MyAccountManager(BaseUserManager):

    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        usr = self.create_user(
            password=password,
            username=username,
        )
        usr.is_admin = True
        usr.is_staff = True
        usr.is_superuser = True
        usr.save(using=self._db)
        return usr



class user(AbstractBaseUser):
    username = models.CharField(max_length=30, primary_key=True, unique=True)
    password = models.CharField(max_length=100)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=16, null=True)
    choice = [("m", "man"),("w", "woman")]
    gender = models.CharField(max_length=1, choices=choice)
    parent_of = models.ForeignKey(family,related_name="parent_of", null=True, on_delete=SET_NULL)
    child_of = models.ForeignKey(family, null=True,related_name="child_of", on_delete=SET_NULL)
    pg = models.ForeignKey(package, null=True, on_delete=SET_NULL)
    last_login	= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'

    objects = MyAccountManager()

    def __str__(self):
       return self.username

	# For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
       return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True



@receiver(post_save, sender=AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
    

