import os
from dotenv import load_dotenv
from openai import OpenAI

import requests
import json
import time

load_dotenv() # .env file se data load karne ke liye
api_key = os.getenv ('OPENROUTER_API_KEY')

# Check karne ke liye (Optional):
if not api_key:
    print("Masla: API Key nahi mili! Check karein ke .env file bani hai ya nahi.")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key
)

def ask_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Sales Expert Agent"
    }
    
    data = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": [
            {
                "role": "system", 
                "content": """You are a world-class Sales & Cold Outreach Expert. 
                Your goal is to write highly persuasive, short, and professional emails 
                that get a 100% response rate. Use emotional triggers and clear Call to Actions."""
            },
            {
                "role": "user", 
                "content": f"Write a cold email for this: {prompt}"
            }
        ],
        "temperature": 0.7 # Ye AI ko creative banata hai
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Connection Error: {e}"

# --- Main Loop ---
print("--- OpenRouter Requests Method Active ---")
while True:
    user_query = input("\nSawal likhein (exit to stop): ")
    if user_query.lower() == 'exit':
        break
        
    jawab = ask_ai(user_query)
    print("\nAI ka Jawab:", jawab)