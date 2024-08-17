from django.shortcuts import render
from .models import Event
from django.utils import timezone

# Create your views here.
def count_timer(request):
    #The method retrieves first object of the class Event 
    remaining_event = Event.objects.first()
    
    #If event object is fetched then we calculate the remaining time and store it to a Dictionary object 
    if remaining_event:
        remaining_time = remaining_event.event_date - timezone.now()
        
        hours = remaining_time.seconds // 3600
        minutes = (remaining_time.seconds % 3600) // 60
        seconds = remaining_time.seconds % 60
        
        time ={
            'name':remaining_event.name,
            'hours':hours,
            'minutes':minutes,
            'seconds':seconds,
        }
    else:
        #If event object is not fetched then we store default value to a Dictionary object
                time ={
            'name':"No Event",
            'hours':0,
            'minutes':0,
            'seconds':0,
        }
                
    return render(request,'index.html',{'time':time})