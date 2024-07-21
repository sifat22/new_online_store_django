from django.contrib import admin
from .models import Product,Variation
from django.contrib.auth.models import User

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug' :('product_name',)}
    list_display = ('product_name','stock','is_available','offers','price','modified_date',)
    
            
            
            

#for variation

class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", "variation_category", "variation_value" , "is_active")
    list_editable =("is_active",)
    list_filter = ("product", "variation_category", "variation_value" )





admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
