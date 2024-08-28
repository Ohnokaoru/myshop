from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem
from userprofile.models import UserProfile

# Create your views here.
"""
購物流程:商品加入購物車->檢視購物車->確認訂單(按鈕)->創建Order與OrderItem->清空購物車
->寄送信件
"""


# 預覽訂單資訊
@login_required
def view_order(request):
    # 購物車內容
    cart_items = CartItem.objects.filter(user=request.user)
    if len(cart_items) == 0:
        return redirect("index")

    # 生成訂單（不保存）
    order = Order(user=request.user)

    total_amount = 0
    order_items = []

    for cart_item in cart_items:
        order_item = OrderItem(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.product_price,
        )

        order_items.append(order_item)
        total_amount += cart_item.product.product_price * cart_item.quantity

    order.total_amount = total_amount

    # 更改地址
    if request.method == "POST":
        new_address = request.POST.get("shipping_address")
        if new_address:
            order.shipping_address = new_address
            # 將新寄送地址以session保存
            request.session["shipping_address"] = new_address

    # 使用基本資料的地址
    else:
        userprofile = UserProfile.objects.get(user=request.user)
        userprofile_address = userprofile.address
        order.shipping_address = userprofile_address

    return render(
        request,
        "order/view-order.html",
        {"order": order, "order_items": order_items},
    )


# 下訂單
@login_required
def confirm_order(request):
    # 購物車內容
    cart_items = CartItem.objects.filter(user=request.user)

    if len(cart_items) == 0:
        return redirect("index")

    # 建立訂單
    order = Order.objects.create(user=request.user)

    total_amount = 0
    order_items = []
    for cart_item in cart_items:
        # 建立OrderItem抓取購物車內容
        order_item = OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.product_price,
        )
        order_items.append(order_item)

        total_amount += cart_item.product.product_price * cart_item.quantity

    order.total_amount = total_amount
    order.status = "pending"

    # .session.get()，如果沒有值會反為None
    new_address = request.session.get("shipping_address")
    if new_address:
        order.shipping_address = new_address

    else:
        userprofile = UserProfile.objects.get(user=request.user)
        userprofile_address = userprofile.address
        order.shipping_address = userprofile_address

    order.save()

    # 清除 session 中的地址
    if "shipping_address" in request.session:
        del request.session["shipping_address"]

    # 清空購物車
    cart_items.delete()

    return render(
        request,
        "order/confirm-order.html",
        {"order": order, "order_items": order_items},
    )
