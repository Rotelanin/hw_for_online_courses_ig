from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from django.http import HttpResponse

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    response = render(request, "main/product_detail.html", {"product": product})
    response.set_cookie("last_product", product.id, max_age=3600)
    return response

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "main/add_product.html", {"form": form})

def product_list(request):
    products = Product.objects.all()
    return render(request, "main/product_list.html", {"products": products})
