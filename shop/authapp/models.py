from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    age = models.PositiveIntegerField('возраст', null=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    email = models.EmailField(('email_address'), unique=True)