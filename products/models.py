from django.db import models
from core import modelFieldChoicesManager as MCM


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=128)
    model_number = models.CharField(max_length=128)
    product_category = models.CharField(max_length=5 ,choices = MCM.PRODUCT_CATEGORY_CHOICES())
    product_type = models.CharField(max_length=128)
    manufacturer = models.CharField(max_length=128)
    mrp = models.CharField(max_length=128)
    #offers etc..

    def __str__(self):
        return self.product_name