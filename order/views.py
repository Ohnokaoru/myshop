from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem
from userprofile.models import UserProfile
from product.models import Product
import smtplib
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import math

# Create your views here.
"""
購物流程:商品加入購物車->檢視購物車->確認訂單(按鈕)->創建Order與OrderItem->更改地址->清空購物車
->寄送信件
"""


# 預覽訂單資訊
@login_required
def view_order(request):
    message = ""
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
            message = "地址更改成功!!!"

    # 使用基本資料的地址
    else:
        userprofile = UserProfile.objects.get(user=request.user)
        userprofile_address = userprofile.address
        order.shipping_address = userprofile_address

    return render(
        request,
        "order/view-order.html",
        {"order": order, "order_items": order_items, "message": message},
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

        # 更新庫存數量
        if cart_item.product.product_stock >= cart_item.quantity:
            cart_item.product.product_stock -= cart_item.quantity
            cart_item.product.save()

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

    # 寄送訂單郵件

    subject = "感謝您在myshop消費"
    # 寄件者
    sender_email = "x06nk4alau@gmail.com"
    # 收件者
    receiver_email = request.user.userprofile.email

    # 使用 Django 的模板系統來渲染郵件的內容(html)
    content = render_to_string(
        "order/confirm-order.html", {"order": order, "order_items": order_items}
    )

    # 純文字
    content_plain = strip_tags(content)

    # 支持多格式
    email = EmailMultiAlternatives(
        subject=subject,
        # 純文字內容
        body=content_plain,
        from_email=sender_email,
        to=[receiver_email],
    )

    # 附加HTML內容作為郵件的另一種格式
    email.attach_alternative(content, "text/html")

    # 發送郵件
    try:
        email.send()
        print("email成功發送")
    except Exception as e:
        print(f"發送錯誤: {e}")

    return render(
        request,
        "order/confirm-order.html",
        {"order": order, "order_items": order_items},
    )


# 查詢歷史訂單
@login_required
def get_orders(request):
    message = ""

    orders = Order.objects.filter(user=request.user).order_by("-order_time")

    total_order = len(orders)
    if total_order == 0:
        message = "沒有購物紀錄"

    page_size = 5
    page = int(request.GET.get("page", 1))
    total_page = math.ceil(total_order / page_size)
    page_btn = request.GET.get("page_btn", "")

    # 合理頁數
    if page > total_page:
        page = total_page

    if page < 1:
        page = 1

    # 點擊頁數
    # 上一頁
    if page_btn == "prev" and page > 1:
        page -= 1

    # 下一頁
    elif page_btn == "next" and page < total_page:
        page += 1

    # 計算頁數
    start = (page - 1) * page_size
    end = start + page_size
    orders = Order.objects.filter(user=request.user).order_by("-order_time")[start:end]

    next = page < total_page
    prev = page > 1

    # 將每一筆order有多筆order_item，將所有相同id的物件存一起
    order_items_dict = {}
    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        order_items_dict[order.id] = order_items

    return render(
        request,
        "order/get-orders.html",
        {
            "page": page,
            "total_page": total_page,
            "orders": orders,
            "prev": prev,
            "next": next,
            "order_items_dict": order_items_dict,
            "message": message,
        },
    )
