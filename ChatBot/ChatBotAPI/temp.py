import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(
    api_key=os.environ['GoogleAPIKey'])
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash')
chat = model.start_chat()
print("You: ","Hello.")
response = chat.send_message(
          "Hello.")
print("AI: ",response.text)

print("You: ","Just chillin'")
response = chat.send_message(
          "Just chillin'")
print("AI: ",response.text)
        