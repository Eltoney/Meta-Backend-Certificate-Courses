from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    inventory = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.title
    