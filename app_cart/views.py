from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from app_store.models import Product,Variation
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
#get the session id for cart
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id = product_id)  #get the product
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:   #get the item and its value
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product = product, variation_category__iexact=key, variation_value__iexact= value)# iexact means value or key can be capital or small letter
                product_variation.append(variation)
            except:
                pass

            
    
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request) )  # get the cart using the cart id present in session

    except Cart.DoesNotExist:
        cart =  Cart.objects.create(
            cart_id =_cart_id(request)
        )
    cart.save()


    try:
        cart_item = CartItem.objects.get(product = product,cart=cart)
        if len(product_variation) > 0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variation.add(item)

        cart_item.quantity +=1 #cart_item.quantity = cart_item.quantity +1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        if len(product_variation) > 0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variation.add(item)
        cart_item.save()
    return redirect("cart")

# decrement the cartr
def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product = product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart")

#delete the cart
def delete_cart(request,product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product = product, cart=cart)
    cart_item.delete()
    return redirect("cart")


def cart(request, total=0, quantity=0, cart_items = None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id =_cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart , is_active=True)

        for cart_item in cart_items:
            total += (cart_item.discout_price() * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    return render(request,"app_cart/cart.html",{
        "total" :round(total,2),
        "quantity" : quantity,
        "cart_items" :cart_items ,
        "tax" :round(tax,2),
        "grand_total" : round(grand_total, 2),
    })
