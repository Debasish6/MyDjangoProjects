from django.shortcuts import render, HttpResponse
from django.contrib.sessions.models import Session
from .models import ChatSession
from .tasks import process_chatbot_request
from .main import ChatBot
from dotenv import load_dotenv
import os, sys, json
from celery.result import AsyncResult

load_dotenv()

def home(request):
    return HttpResponse("<h1>Welcome to Our ChatBot Web Application</h1>")

def chatbot(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt_text', '')  # Use get to avoid KeyError

        # Get current session or create a new one
        session_id = request.session.session_key
        chat_session, created = ChatSession.objects.get_or_create(session_id=session_id)
        chat_history = chat_session.chat_history

        # Process request asynchronously
        task = process_chatbot_request.delay(session_id, prompt)

        # Update chat history with user prompt
        if prompt.lower() != 'bye':
            chat_history.append({'user': prompt, 'ai': 'Processing...'})

        chat_session.chat_history = chat_history
        chat_session.save()

        context = {
            'history': chat_history,
            'task_id': task.id,  # Pass task ID to the template
        }
        return render(request, "index.html", context)

    # Render the template with chat history on GET requests
    session_id = request.session.session_key
    chat_session = ChatSession.objects.get_or_create(session_id=session_id)[0]
    chat_history = chat_session.chat_history
    context = {
        'history': chat_history,
        'task_id': None,
    }
    return render(request, "index.html", context)

def get_chatbot_response(request, task_id):
    task_result = AsyncResult(task_id)
    if task_result.state == 'SUCCESS':
        response_data = task_result.result
    else:
        response_data = 'Processing...'

    return HttpResponse(json.dumps({'ai_data': response_data}), content_type='application/json')
