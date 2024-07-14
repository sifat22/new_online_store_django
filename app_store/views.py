from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from.models import Product
from app_brand.models import Brand
from app_category.models import Category
from django.db.models import Sum
from app_wishlist.views import _wishlist_id, product_in_wishlist

from app_wishlist.models import WishlistItem


# Create your views here.


def store(request, brand_slug=None, category_slug=None):
    products = None
    categories = None
    brands = None
    #in_wishlist = False
    
    if category_slug:
        categories = get_object_or_404(Category, slug = category_slug)
        brands = get_object_or_404(Brand, slug = brand_slug)
        products = Product.objects.filter(category = categories, is_available= True)
        cat_by_brand = Category.objects.filter(brand = brands)

        product_count = products.count()

    elif brand_slug:
        brands = get_object_or_404(Brand, slug = brand_slug)
        products = Product.objects.filter(brand = brands, is_available= True)
        cat_by_brand = Category.objects.filter(brand = brands)
        product_count = products.count()

    # elif brand_slug and brand_slug:
    #     brands = get_object_or_404(Brand, slug = brand_slug)
    #     categories = get_object_or_404(Category, slug = category_slug)
    #     products = Product.objects.filter(brand = brands, category = categories, is_available= True)
    #     product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by("-modified_date")
        cat_by_brand = Category.objects.all()[:0]
        product_count = products.count()

    # try:
    #     single_product = get_object_or_404(Product, slug=product_in_wishlist)
    #     in_wishlist = WishlistItem.objects.filter(product = single_product).exists()
    # except:
    #     pass
    
        



    return render(request,"app_store/store.html",{
        "products" : products,
        "product_count" : product_count,
        "cat_by_brand" : cat_by_brand,
        #"in_wishlist" : in_wishlist,
        # "product_slug" : product_slug
       

    })


#in wishlist or not

# def in_wishlist_item(request, brand_slug, category_slug, product_slug):
#     context = {}
#     try:
#         single_product = get_object_or_404(Product, brand__slug = brand_slug, category__slug = category_slug, slug = product_slug)
#         in_wishlist = WishlistItem.objects.filter(wishlist__wishlist_id = _wishlist_id(request), product = single_product).exists()
      

#     except Exception as e:
#         raise e
    
#     context.update({
#             'in_wishlist': in_wishlist,
#         })

        
        
        






def product_details(request, brand_slug, category_slug, product_slug):
    total_stock = 0
    try:
        product_detail = get_object_or_404(Product, brand__slug = brand_slug, category__slug = category_slug, slug = product_slug)
        total_stock = product_detail.stock
        
      

    except Exception as e:
        raise e
    return render(request,"app_store/product_details.html",{
        "product_detail" : product_detail,
        "total_stock" : total_stock,
        
        
        
        
    })