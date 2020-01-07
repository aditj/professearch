from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_login = models.DateTimeField(null=True, blank=True)
    verify_captcha=models.BooleanField()

# Create your models here.


class Prof(models.Model):
    name = models.CharField(max_length=255)
    institute = models.CharField(max_length=255)
    dept = models.CharField(max_length=255)
    aor = models.TextField(null=True)
    phone = models.CharField(max_length=25,null=True)
    email = models.CharField(max_length=255,null=True)
    web = models.CharField(max_length=512,null=True)


    def __str__(self):
        return self.name
