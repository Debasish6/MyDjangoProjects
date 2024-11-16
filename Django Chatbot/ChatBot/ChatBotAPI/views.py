from django.shortcuts import render,HttpResponse
from rest_framework.decorators import api_view
from ChatBotAPI.chatbot import ChatBot
from ChatBotAPI.main import main_function
import sys
import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("GoogleAPIKey")

chatbot = ChatBot(api_key=api_key)
chatbot.start_conversation()
print("Welcome to Expand smERP Chat bot. Type 'bye' to exit.")
# choice =int(input("1.Product Related Questions\n2.Company and ERP Software Related Questions\n"))
chatbot.previous_db_results = []

# Create your views here.
def home(request):
    return render(request,'index.html')

# @api_view(['POST'])
def chatBot_api_view(request):
    if request.method == 'POST':
        message = request.POST.get('userinput')
        print(message)

        while True:
            user_input = message
            if user_input.lower() =='bye':
                response = chatbot.send_prompts(user_input,chatbot.previous_db_results)
                print(f"\n{chatbot.CHATBOT_NAME}: {response}")
                chatbot.previous_db_results = []
                sys.exit("............Exiting ChatBot..........")
            try:
                response = chatbot.send_prompts(user_input,chatbot.previous_db_results)
                print(f"\n{chatbot.CHATBOT_NAME}: {response}")
            except Exception as e:
                response = "Some Error"
                print(f'Error: {e}')
            context={
                'data': response
            }
            return render(request,'result.html',context)

    return render(request, "index.html")



