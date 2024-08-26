from django.shortcuts import render

# Create your views here.
def home(request):
    if request.method == 'POST':
        text = request.POST['translate']
        lang = request.POST['language']
    return render(request,'translate.html')