import google.generativeai as genai
from django.conf import settings 

# Assume settings.GEMINI_API_KEY is where the API key for Gemini is stored 
gemini_api_key = settings.APIKEY
system_instruction = settings.SYSTEM_INSTRUCTION

generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 2048,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]

model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    safety_settings=safety_settings,
                    generation_config=generation_config,
                    system_instruction=system_instruction,
                )