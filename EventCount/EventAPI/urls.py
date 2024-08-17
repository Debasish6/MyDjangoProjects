from django.urls import path
from . import views

urlpatterns = [
    path('',views.count_timer,name='count_timer'),
]
