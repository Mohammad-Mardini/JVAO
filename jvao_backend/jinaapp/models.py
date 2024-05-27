from django.db import models

# Create your models here.
class JinaBase(models.Model):
    x_value = models.CharField(max_length=250)
    y_value = models.CharField(max_length=250)

