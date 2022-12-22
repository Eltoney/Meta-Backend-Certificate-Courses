from django.db import models

# Create your models here.


class Food(models.Model):
    name = models.CharField(max_length=255)
    category = models.IntegerField()
    price = models.IntegerField()


    def __str__(self):
        return self.name
    