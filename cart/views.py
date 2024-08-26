from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem
from product.models import Product


# Create your views here.


# 加入購物車
@login_required
def add_cart(request, product_id):
    message = ""
    try:
        product = Product.objects.get(id=product_id)

    except Product.DoesNotExist:
        return redirect("index")

    # 庫存
    if product.product_stock == 0:
        message = "目前缺貨中"

    try:
        cart_item = CartItem.objects.get(user=request.user, product=product)
        cart_item.quantity += 1
        if cart_item.quantity == product.product_stock:
            message = "添加數量已經最大囉!"
        else:
            cart_item.save()
            message = "商品已在購物車，數量+1"

    # 手動增加(不使用form)
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(user=request.user, product=product)
        cart_item.quantity = 1
        message = "新增商品到購物車"

    return redirect("index")


# 檢視購物車內容
@login_required
def view_cart(request):
    cart_items = CartItem.objects.all()

    if len(cart_items) == 0:
        return redirect("index")

    return render(render, "cart/view-cart.html", {"cart_items": cart_items})
