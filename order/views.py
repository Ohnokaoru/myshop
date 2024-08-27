from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem

# Create your views here.
"""
購物流程:商品加入購物車->檢視購物車->確認訂單(按鈕)->創建Order與OrderItem->清空購物車
->寄送信件
"""


# 確認訂單
@login_required
def confirm_order(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items:
        return redirect("index")

    # 建立Order訂單
    order = Order.objects.create(user=request.user)

    total_amount = 0
    # 將購物車項目轉為訂單項目(建立OrderItem，每個order都是一種商品訂單項目)
    for cart_item in cart_items:
        order_item = OrderItem.objects.create(
            order=order, product=cart_item.product, quantity=cart_item.quantity
        )

        # 計算總金額
        total_amount += cart_item.quantity * cart_item.product.product_price

    # 更新Order訂單的總金額
    order.total_amount = total_amount
    order.status = "pending"
    order.save()

    # 清空購物車
    cart_items.delete()

    return render(
        request,
        "order/confirm-order.html",
        {"order": order, "order_item": order_item},
    )
