from django.shortcuts import render,HttpResponse
from pytube import *

# Create your views here.
def home(request):
   if request.method == 'POST':
      link = request.POST['link']
      video = YouTube(link)
      
      stream = video.streams.get_lowest_resolution()
      stream.download()
      return render(request,'index.html')
   return render(request,'index.html')