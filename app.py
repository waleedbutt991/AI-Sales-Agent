import streamlit as st
import os
from dotenv import load_dotenv
import requests
import json

# Page configuration
st.set_page_config(page_title="AI Sales Outreach Agent", page_icon="✉️")

load_dotenv()
# Streamlit Cloud par ye 'st.secrets' se uthayega, local par '.env' se
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
            {
                "role": "system", 
                "content": "You are a world-class Sales & Cold Outreach Expert. Write highly persuasive, concise, and professional cold emails. Focus on benefits and a clear call to action."
            },
            {"role": "user", "content": f"Generate a high-converting cold email based on these details: {prompt}"}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()['choices'][0]['message']['content']

# --- UI Design ---
st.title("🚀 AI Sales Outreach Agent")
st.markdown("### Elevate your sales game with high-converting cold emails.")

# Input section
st.divider()
user_prompt = st.text_area(
    "Describe your offer and target audience:", 
    placeholder="Example: Selling high-end SEO services to Dental Clinics in New York...",
    height=150
)

# Execution section
if st.button("Generate Professional Email"):
    if user_prompt:
        with st.spinner("Our AI Expert is crafting your email..."):
            try:
                email_content = ask_ai(user_prompt)
                st.success("Your email is ready!")
                
                # Output Display
                st.subheader("Generated Email Draft")
                st.text_area("", value=email_content, height=400)
                
                # Actions
                st.download_button(
                    label="📥 Download Email Draft",
                    data=email_content,
                    file_name="cold_email.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please provide some details about your outreach target.")

st.divider()
st.caption("Powered by Llama 3.3 | Developed for Professional Sales Teams")
