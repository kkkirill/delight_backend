from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models import (
    BooleanField, CharField, EmailField, IntegerField,
    ManyToManyField, URLField)

from delight.settings import STATIC_CLOUDFRONT_DOMAIN, DEFAULT_USER_LOGO_FILENAME
from delight.validators import CustomURLValidator


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_staff=False,
                    is_superuser=False):

        if not username:
            raise ValueError("Users must have the username")
        if not email:
            raise ValueError("Users must have the email")
        if not password:
            raise ValueError("Users must have the password")

        user = self.model(username=username,
                          email=self.normalize_email(email))
        user.set_password(password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_staffuser(self, username, email, password=None):
        user = self.create_user(username, email, password, is_staff=True)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password, is_staff=True,
                                is_superuser=True)
        user.is_superuser = True
        return user


class User(AbstractBaseUser):
    username = CharField(max_length=50, unique=True)
    email = EmailField(max_length=50, unique=True)
    photo = URLField(default=f'{STATIC_CLOUDFRONT_DOMAIN}/default/{DEFAULT_USER_LOGO_FILENAME}',
                     validators=[CustomURLValidator])
    followers = ManyToManyField('User', blank=True, related_name='following')
    followers_amount = IntegerField(default=0)
    is_staff = BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    objects = UserManager()

    def __str__(self):
        return self.username
