from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
from .form import Productform

# Create your views here.
#All product view
def product_items(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})

#Single Product View
def single_product_item(request,pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request,'index.html',{'product':product})

#Edit the product
def edit_product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    
    if request.method == 'POST':
        form = Productform(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form =Productform(instance=product)
    return render(request,'edit.html',{'form':form,'product':product}) 

def delete_product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')       
    return render(request, 'delete.html',{'product':product})