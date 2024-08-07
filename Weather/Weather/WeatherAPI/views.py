from django.shortcuts import render
import json
import urllib.request

# Create your views here.
def home(request):
    if request.method == 'POST':
        city = request.POST['city']
        
        #It returns JSON data
        json_data = urllib.request.urlopen('http://api.weatherapi.com/v1/current.json?key=a5bb573037984034ac905523240708&q='+city).read()
        
        #Converting JSON data to dict
        whole_data = json.loads(json_data)
        
        data ={
            'country': str(whole_data['location']['country']),
            'coordinate': str(whole_data['location']['lat']) + ' ' + str(whole_data['location']['lon']),
            'temp':str(whole_data["current"]['temp_c'])+ 'C',
            'pressure':str(whole_data["current"]['pressure_mb']),
            'humidity':str(whole_data["current"]['humidity']),
        }
        
        print(data)
    else:
        data={}
    return render(request,"index.html",data)