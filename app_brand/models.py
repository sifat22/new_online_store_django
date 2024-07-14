from django.db import models
from django.urls import reverse


# Create your models here.


class Brand(models.Model):
    brand_name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(unique=True)


    def get_url(self):
        return reverse("products_by_brand", args =[self.slug])




    def __str__(self):
        return self.brand_name
    

