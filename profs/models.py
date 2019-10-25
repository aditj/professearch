from django.db import models

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
