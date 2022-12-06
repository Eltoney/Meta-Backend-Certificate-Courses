from django.db import models

# Create your models here.


class Drinks(models.Model):
    name = models.CharField(max_length=10)
    price = models.IntegerField()
