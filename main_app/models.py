from django.db import models
class contact(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    country=models.CharField(max_length=100)
    subject=models.TextField()
# Create your models here.
