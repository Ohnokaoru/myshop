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
        if cart_item.quantity < product.product_stock:
            cart_item.quantity += 1
            cart_item.save()
            message = "商品已在購物車，數量+1"

        else:
            message = "添加數量已經最大囉!"

    # 手動增加(不使用form)
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(user=request.user, product=product)
        cart_item.quantity = 1
        message = "新增商品到購物車"

    return redirect("index")


# 檢視購物車內容
@login_required
def view_cart(request):

    # 處理庫存小於數量問題
    message = ""
    cart_items = CartItem.objects.filter(user=request.user)

    if len(cart_items) < 1:
        message = "購物車沒項目，請繼續購物"

    total_amount = 0
    for cart_item in cart_items:

        if cart_item.product.product_stock == 0:
            cart_item.delete()

        elif cart_item.quantity > cart_item.product.product_stock:
            message = f"你的{cart_item.product.product_name}需求大於庫存量，已幫你更新為最大庫存量"
            cart_item.quantity = cart_item.product.product_stock
            cart_item.save()

        item_money = int(cart_item.quantity) * int(cart_item.product.product_price)
        total_amount += item_money

    # 更新商品清單
    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == "POST":
        clear_all = request.POST.get("clear_all")
        cart_items.delete()
        message = "購物車沒項目，請繼續購物"

    # 是否可以出現下訂單鈕
    if total_amount > 0:
        have_total_amount = total_amount
    else:
        have_total_amount = None

    return render(
        request,
        "cart/view-cart.html",
        {
            "cart_items": cart_items,
            "total_amount": total_amount,
            "have_total_amount": have_total_amount,
            "message": message,
        },
    )


# 修改與刪除購物車(手動修改儲存)
@login_required
def edit_cart(request, product_id):
    try:
        cart_item = CartItem.objects.get(id=product_id, user=request.user)
    except CartItem.DoesNotExist:
        return redirect("view-cart")

    if request.method == "POST":
        button = request.POST.get("button")

        if button == "修改":
            quantity = int(request.POST.get("quantity"))

            # 存檔
            cart_item.quantity = quantity
            cart_item.save()
            return redirect("view-cart")

        elif button == "刪除":
            cart_item.delete()
            return redirect("view-cart")

    else:
        quantity = cart_item.quantity

    return render(
        request, "cart/edit-cart.html", {"cart_item": cart_item, "quantity": quantity}
    )
