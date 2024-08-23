from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProductForm
from .models import Product
import math

# Create your views here.


# 新增商品
@staff_member_required
def create_product(request):
    message = ""
    if request.method == "POST":
        # 提交文字與文件(ex:圖片)
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            productform = form.save()
            print("Uploaded file path:", productform.product_img.path)
            return redirect("index")

        else:
            message = "資料錯誤"

    else:
        form = ProductForm()

    return render(
        request, "product/create-product.html", {"form": form, "message": message}
    )


# 檢視所有商品(首頁)
def index(request):
    products = Product.objects.all().order_by("id")
    total_product = len(products)
    if total_product < 1:
        return redirect("create-product")

    page_size = 4
    total_page = math.ceil(total_product / page_size)
    page = int(request.GET.get("page", 1))
    page_btn = request.GET.get("page_btn", "")

    # 合理頁數
    if page < 1:
        page = 1

    if page > total_page:
        page = total_page

    # 點擊上一頁
    if page_btn == "prev" and page > 1:
        page -= 1

    # 點擊下一頁
    if page_btn == "next" and page < total_page:
        page += 1

    # 計算頁數
    start = (page - 1) * page_size
    end = start + page_size
    products = Product.objects.all().order_by("id")[start:end]

    next = page < total_page
    prev = page > 1

    # 將員工與一般使用者分為兩個介面
    if request.user.is_staff:
        template = "product/index-staff.html"

    else:
        template = "product/index.html"

    return render(
        request,
        template,
        {
            "products": products,
            "page": page,
            "total_page": total_page,
            "next": next,
            "prev": prev,
        },
    )


# 修改商品
@staff_member_required
def edit_product(request, product_id):
    message = ""
    try:
        product = Product.objects.get(id=product_id)

    except Product.DoesNotExist:
        return redirect("index")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            productform = form.save()
            print("Uploaded file path:", productform.product_img.path)
            return redirect("index")

        else:
            message = "資料錯誤"

    else:
        form = ProductForm(instance=product)

    return render(
        request, "product/edit-product.html", {"form": form, "message": message}
    )


# 刪除商品
@staff_member_required
def delete_product(request, product_id):
    message = ""
    product = None
    try:
        product = Product.objects.get(id=product_id)

    except Product.DoesNotExist:
        return redirect("index")

    if request.method == "POST":
        product.delete()
        message = "刪除商品成功"

    return render(
        request, "product/delete-product.html", {"message": message, "product": product}
    )
