import streamlit as st
import os
from dotenv import load_dotenv
import requests
import json

# Page ki setting (title aur icon)
st.set_page_config(page_title="Sales AI Agent", page_icon="💰")

load_dotenv()
api_key = os.getenv('OPENROUTER_API_KEY')

def ask_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a world-class Sales Expert. Write persuasive emails."},
            {"role": "user", "content": f"Write a cold email for: {prompt}"}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()['choices'][0]['message']['content']

# --- UI Design ---
st.title("🚀 Sales Expert AI Agent")
st.subheader("Likhein kiske liye email chahiye, Agent khud likh dega!")

# Input field
user_prompt = st.text_area("Yahan details likhein (e.g. Selling SEO services to a dentist):", placeholder="Enter your product/service details...")

# Button
if st.button("Generate Cold Email"):
    if user_prompt:
        with st.spinner("Agent soch raha hai..."):
            try:
                email_content = ask_ai(user_prompt)
                st.success("Email Taiyar Hai!")
                # Result ko box mein dikhana
                st.text_area("AI Generated Email:", value=email_content, height=300)
                # Copy button ka kaam bhi asaan ho jata hai
                st.download_button("Download Email as Text", email_content)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Pehle kuch likhein to sahi!")
