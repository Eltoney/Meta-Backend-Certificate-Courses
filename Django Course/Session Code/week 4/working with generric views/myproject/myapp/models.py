from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    class Meta:
        db_table = "Employee"
    def __str__(self) -> str:
        return self.name

