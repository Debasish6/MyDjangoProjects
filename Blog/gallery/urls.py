from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.product_items,name='product_list'),
    path('<int:pk>/',views.single_product_item,name='product_details'),
]