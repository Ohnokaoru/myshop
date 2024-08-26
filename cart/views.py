from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem
from product.models import Product
from django.core.exceptions import ValidationError

# Create your views here.


# 加入購物車
@login_required
def add_cart(request, product_id):
    message = ""
    try:
        product = Product.objects.get(id=product_id)

    except Product.DoesNotExist:
        return redirect("index")

    try:
        cart_item = CartItem.objects.get(user=request.user, product=product)
        cart_item.quantity += 1
        cart_item.save()
        message = "商品已在購物車，數量+1"

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(user=request.user, product=product)
        cart_item.quantity = 1
        message = "新增商品到購物車"

    return redirect("index")
