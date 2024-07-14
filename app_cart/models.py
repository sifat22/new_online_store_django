from django.db import models
from app_store.models import Product,Variation

# Create your models here.

class Cart(models.Model):
    cart_id =  models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


    
    
    def discout_price(self):
        return  self.product.price - ((self.product.offer_precentage * self.product.price)/100)
    
    def sub_total(self):
        sub_total = self.discout_price() * self.quantity
        return round(sub_total, 2)


    def __unicode__(self):
        return self.product




