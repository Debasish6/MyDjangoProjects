from django.shortcuts import render, HttpResponse
from translate import Translator

# Create your views here.

def home(request):
    if request.method == 'POST':
        text = request.POST['translate']
        lang = request.POST['language']
        model = Translator(to_lang=lang)
        translated_text = model.translate(text)
        return render(request,'translate.html',{'context':translated_text})
    return render(request,'translate.html')