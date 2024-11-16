# Chat Bot using Gemini model

import pyodbc
import sqlalchemy
from sqlalchemy import create_engine,text
from configparser import ConfigParser
import google.generativeai as genai
from dotenv import load_dotenv
import os,re,json

load_dotenv()
system_instruction = os.environ.get("system_instruction")

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

class GenAIExeption(Exception):
    """GenAI Exception base class"""

class ChatBot:
    CHATBOT_NAME = 'AI Assistant'

    def __init__(self,api_key):
        self.genai = genai
        self.genai.configure(
            api_key=api_key
        )
        self.model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    safety_settings=safety_settings,
                    generation_config=generation_config,
                    system_instruction=system_instruction,
                )
        self.conversation = None
        self.dbflag = False 
        self._conversation_history = []
        self.preload_conversation()
        self.db_engine = self.setup_db_connection()
        self.previous_db_results = []
        self.count = 0

    def get_gemini_response(self, question, conversation_history, previous_db_results): 
        formatted_results = self.format_results(previous_db_results) 
        context = f"Previous results:\n{formatted_results}\n\nNew question: {question}" 
        response = self.model.generate_content([context]) 
        response.resolve() 
        return response.text

    

    def _generation_config(self,temperature):
        return genai.types.GenerationConfig(
            temperature=temperature
        )
    
    
    
    def setup_db_connection(self):
        db_username = os.environ.get("db_username")
        db_password = os.environ.get("db_password")
        db_host = os.environ.get("db_hostname")
        db_name = os.environ.get("db_database")
        db_server = os.environ.get("db_server")

        connection_string = f"mssql+pyodbc://{db_username}:{db_password}@{db_server}/{db_name}?driver=ODBC Driver 17 for SQL Server"
        engine = create_engine(connection_string)
        return engine
    
    def handle_response(self, response):
        # Blocking potentially dangerous operations
        dangerous_keywords = ["UPDATE", "DELETE", "DROP", "TRUNCATE", "CREATE"]
        safe_phrase = "EXPAND"
        if any(keyword in response.upper() for keyword in dangerous_keywords) and (safe_phrase not in response.upper() and not response.startswith("SELECT")):
            print(response)
            return "This operation is Not Possible."
        
        # Process non-SELECT responses
        if not response.strip().upper().startswith("SELECT"):
            # This is improved version of splitting
            cleaned_query = response.replace("```sql", "").replace("```","").strip()
            response = cleaned_query
              
        
        # Execute the query if it starts with SELECT
        if response.strip().upper().startswith("SELECT") or response.strip().upper().startswith("WITH RANKEDPRODUCTS"):
            print(f"Executing query: {response}")
            db_results = self.execute_queries(response)

            formatted_result = {"text": "\n".join([str(row) for row in db_results])}
            return formatted_result
        else:
            return {"text": response}
            
    
    def sanitize_input(self,user_input):
        # Only allow alphanumeric characters and spaces
        sanitized_input = re.sub(r'[^a-zA-Z0-9\s/-]', '', user_input)
        return sanitized_input
    
    def format_results(self, results): 
        return "\n".join([", ".join(map(str, row)) for row in results])
        

    
    
    
    def send_prompts(self, user_input,previous_db_results, temperature=0.5):
        if(temperature<0 or temperature >1):
            raise GenAIExeption('Temperature must be between 0 and 1')
        if not user_input:
            raise GenAIExeption('Prompt can not be empty')
        
        # Sanitize and validate user input 
        user_input = self.sanitize_input(user_input)
        
        bypass_db_queries = ["hi", "hello", "hey", "no", "yes", "bye"]
        if user_input.lower() not in bypass_db_queries:
            try:
                response = self.get_gemini_response(user_input, self._conversation_history, previous_db_results)
                self._conversation_history.append({"role": "user", "content": user_input})
                
                db_results = self.handle_response(response)
                ai_response = json.dumps(db_results, indent=4) if db_results else json.dumps({"text": "No related products found."}, indent=4)
                self._conversation_history.append({"role": "AI Assistant", "content": db_results})
                

            except Exception as e:
                ai_response = json.dumps({"text": f"An error occurred: {str(e)}"}, indent=4)
        else:
            ai_response = self.get_gemini_response(user_input, self._conversation_history, previous_db_results)
            self._conversation_history.append({"role": "AI Assistant", "content": ai_response})
        self.update_chat_history(user_input, ai_response)
        self.save_chat_history()
        return ai_response

    
    # Formatting Database result   
    def format_as_instructions(self, data):
        if data:
            formatted_data = [
                {
                    "Product Number": row[0],
                    "Product Name": row[1],
                    "Product Description": row[2],
                    "Product Back Office Code": row[12],
                    "Vision Number": row[15],
                    "Product UDF7": row[22],
                    "Product UDF8": row[23],
                    "Product Creation Date": row[29].strftime("%Y-%m-%d %H:%M:%S"),
                    "Product Last Update Date": row[30].strftime("%Y-%m-%d %H:%M:%S"),
                    "Product Has Item": row[31],
                    "Product ID": row[40],
                    "Product Band ID": row[42],
                    "UOMID": row[48],
                    "Product Created By User ID": row[49],
                    "Product Updated By User ID": row[50],
                    "Product Property 1ID": row[51],
                    "Component UMOID": row[58],
                    "Prodls Primary": row[62],
                    "Product HSN Code": row[69]
                }
                for row in data
            ]
            json_data = json.dumps(formatted_data, indent=4)
            return f"Here are the related products:\n{json_data}"
        return "No related products found."


    def execute_queries(self, prompt,params={}):
        with self.db_engine.connect() as conn:
            trans = conn.begin()
            try:
                result = conn.execute(
                    text(prompt),params
                ).fetchall()

                # Store the database results
                self.previous_db_results = result
                # self.previous_db_results.append(result)
                # self.count=self.count+1
                # if self.count>=5:
                #     prev_db_results=self.previous_db_results[::-1]
                #     prev_db_results.pop()
                #     self.previous_db_results = prev_db_results[::-1]
                #     self.count=self.count-1
                
                print("Previous Database Results: ",self.previous_db_results)
                return result

                trans.commit()
            except Exception as e:
                trans.rollback()
                raise GenAIExeption(f"Database Error: {str(e)}")
    
    def format_results(self, results):
        return "\n".join([", ".join(map(str, row)) for row in results])

    
    @property
    def history(self,):
        conversation_history = [
            {'role' : message.role, 'text':message.parts[0].text} for message in self.conversation.history
        ]
        return conversation_history

    
    def clear_conversation(self):
        self.conversation = self.model.start_chat(history = [])
    
    def start_conversation(self):
        self.conversation = self.model.start_chat(history = self._conversation_history)
    
    def _construct_message(self,text,role='user'):
        return {'role' : role,'parts':[text]}
    
    def update_chat_history(self, user_input, ai_response): 
        self._conversation_history.append(self._construct_message(user_input, 'user')) 
        self._conversation_history.append(self._construct_message(ai_response, 'ai')) 
        self.save_chat_history() 
        
    def save_chat_history(self, filename='chat_history.json'): 
        with open(filename, 'w') as file: 
            json.dump(self._conversation_history, file, indent=4) 

    def load_chat_history(self, filename='chat_history.json'): 
        try: 
            with open(filename, 'r') as file: 
                self._conversation_history = json.load(file) 
        except FileNotFoundError: 
            self._conversation_history = []
    
    def preload_conversation(self,conversation_history = None):
        if isinstance(conversation_history,list):
            self._conversation_history=conversation_history
        else:
            self._conversation_history = [
                self._construct_message('From now on, return the output as JSON object that can be loaded in Python with the key as \'text\'. For Example, {"text": "<output goes here>"}'),
                self._construct_message('{"text":"Sure, I can return the output as a regular JSON object with the key as `text`. Here is an example {"text":"Your Output"}.','model')
            ]
