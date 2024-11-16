from django.shortcuts import render,HttpResponse
import sys
import os

def main_function(request,chatbot,message):
    while True:
        user_input = message
        if user_input.lower() =='bye':
            response = chatbot.send_prompts(user_input,chatbot.previous_db_results)
            print(f"\n{chatbot.CHATBOT_NAME}: {response}")
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