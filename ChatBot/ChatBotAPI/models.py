from django.db import models

# Create your models here.
class ChatSession(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    chat_history = models.JSONField(default=list)