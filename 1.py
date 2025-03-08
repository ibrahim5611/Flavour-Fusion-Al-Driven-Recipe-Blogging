import streamlit as st
import google.generativeai as genai
import os
import random
import time
from dotenv import load_dotenv

# Load API key securely
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Validate API Key
if not api_key:
    st.error("API key not found! Please set it in the .env file.")
    st.stop()

# Configure the AI model
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate chatbot responses
def chatbot_response(user_query):
    """Generates a response for real-time cooking queries."""
    try:
        prompt = f"You are a cooking assistant. Answer the following question with clear, detailed cooking advice: {user_query}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Sorry, I couldn't fetch an answer right now."

# Streamlit UI
st.set_page_config(page_title="Flavour Fusion", layout="wide")

st.title("Flavour Fusion: AI-Driven Recipe Blogging")
st.subheader("Generate AI-powered recipes with customization, multi-language support, and an interactive chatbot!")

# --- Sidebar Chat Icon ---
with st.sidebar:
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False  # Initial state: chat closed

    if st.button("💬 Cooking Assistant"):
        st.session_state.chat_open = not st.session_state.chat_open  # Toggle chat visibility

# --- Chatbot Window ---
if st.session_state.chat_open:
    st.sidebar.write("## 🍳 Ask me anything about cooking!")
    user_query = st.sidebar.text_input("Type your question:")
    
    if st.sidebar.button("Ask"):
        if user_query:
            response = chatbot_response(user_query)
            st.sidebar.write(f"**Assistant:** {response}")
        else:
            st.sidebar.warning("Please enter a question.")

# --- Main Content ---
st.write("💡 Click the **'💬 Cooking Assistant'** button in the sidebar to ask cooking-related questions in real-time!")
