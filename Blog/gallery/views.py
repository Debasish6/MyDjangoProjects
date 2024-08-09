from django.shortcuts import render,get_object_or_404
from .models import Product

# Create your views here.
#All product view
def product_items(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})

#Single Product View
def single_product_item(request,pk):
    product = Product.objects.all(pk=pk)
    return render(request,'index.html',{'product':product})

# def edit_product(request,product_id):
#     product = get_object_or_404(Product,pk=product_id)
    
#     if request.method == 'POST':
#         form =
    