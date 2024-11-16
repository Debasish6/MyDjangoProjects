from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/',views.chatBot_api_view, name= 'chatbot_api_view')
]
