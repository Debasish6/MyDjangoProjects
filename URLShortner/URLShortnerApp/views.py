from django.shortcuts import render,HttpResponse
import json,requests

# Create your views here.
def home(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        headers = {
            'Authorization':'Bearer 23dc3fe0cd09149fda7d40b7ced6a13aa55d9d05',
            'Content-Type':'application/json'
        }
        data ={
            'long_url':url,
            'domain':'bit.ly'
        }
        
        data = json.dumps(data) #It converts data to json data
        
        response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
        
        short_url=json.loads(response.text)
        print(short_url)
        context ={
            'short-url': short_url['link'],
        }
        return render(request,'index.html',context)
    return render(request,'index.html')