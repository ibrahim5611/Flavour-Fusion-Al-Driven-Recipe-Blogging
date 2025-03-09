import streamlit as st
import google.generativeai as genai
import os
import random
import time
import io
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont

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

# Initialize session state variables
if "recipe_text" not in st.session_state:
    st.session_state.recipe_text = ""
if "food_pairings" not in st.session_state:
    st.session_state.food_pairings = ""
if "translated_ui" not in st.session_state:
    st.session_state.translated_ui = {}

# Function to translate UI dynamically
def translate_text(text, target_language):
    try:
        prompt = f"Translate the following text into {target_language}: {text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return text  # Return original text if translation fails

# Function to update UI translations dynamically
def update_ui_language(selected_language):
    ui_texts = {
        "title": "Flavour Fusion: AI Recipe Generator",
        "settings": "⚙️ Settings",
        "generate_recipe": "Generate Recipe 🍽️",
        "ai_generated_recipe": "📜 AI-Generated Recipe:",
        "food_pairings": "🍷 Food Pairing Suggestions:",
        "ai_chef_qa": "🧑‍🍳 Live Q&A with AI Chef",
        "ask_question": "Ask a question about the recipe:",
        "ask_ai_chef": "Ask AI Chef 🤖",
        "shopping_list": "🛒 Shopping List Generator",
        "enable_shopping_list": "Enable Shopping List",
        "smart_scaling": "🍽️ Smart Recipe Scaling",
        "scale_recipe": "🔄 Scale Recipe",
    }
    
    for key, value in ui_texts.items():
        st.session_state.translated_ui[key] = translate_text(value, selected_language)

# Sidebar for settings
st.sidebar.title("⚙️ Settings")
selected_language = st.sidebar.text_input("🌍 Enter Language (e.g., Spanish, French, Hindi):", "English")
if st.sidebar.button("🌐 Apply Language"):
    update_ui_language(selected_language)

# User Input Section
st.title(st.session_state.get("title", "Flavour Fusion: AI Recipe Generator"))
user_input = st.text_input("Recipe Name (e.g., 'Vegan Chocolate Cake'):", "")
ingredients = st.text_area("Enter Ingredients (comma-separated):", "")
word_count = st.number_input("Enter Word Count:", min_value=100, max_value=2000, step=100, value=500)

# Function to generate a joke dynamically
def get_joke():
    try:
        prompt = "Tell me a unique and funny programming joke ."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Oops! Couldn't fetch a joke this time."

# Function to generate food pairing suggestions
def get_food_pairing(recipe_name):
    try:
        prompt = f"Suggest complementary dishes, drinks, and desserts for {recipe_name}."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "No pairing suggestions available."

# Recipe Generator Function
def generate_recipe():
    if not user_input and not ingredients:
        st.warning("⚠️ Please enter either a recipe topic or ingredients!")
        return
    
    joke = get_joke()
    st.info(f"💡 Joke of the day: {joke}")

    prompt = f"Write a {word_count}-word recipe on {user_input} in {selected_language}."
    if ingredients:
        prompt += f" Use only these ingredients: {ingredients}."
    prompt += " Also, provide a nutritional breakdown."

    try:
        response = model.generate_content(prompt)
        st.session_state.recipe_text = response.text.strip()
        st.session_state.food_pairings = get_food_pairing(user_input)

    except Exception as e:
        st.error(f"Error generating recipe: {e}")

if st.button("Generate Recipe 🍽️"):
    generate_recipe()

if st.session_state.recipe_text:
    st.subheader(st.session_state.translated_ui.get("ai_generated_recipe", "📜 AI-Generated Recipe:"))
    st.write(st.session_state.recipe_text)

    st.subheader(st.session_state.translated_ui.get("food_pairings", "🍷 Food Pairing Suggestions:"))
    st.write(st.session_state.food_pairings)

# Live Q&A with AI Chef
st.subheader(st.session_state.translated_ui.get("ai_chef_qa", "🧑‍🍳 Live Q&A with AI Chef"))
question = st.text_input(st.session_state.translated_ui.get("ask_question", "Ask a question about the recipe:"))

def ask_ai_chef(question):
    try:
        prompt = f"The following is a recipe: {st.session_state.recipe_text}. The user asks: {question}. Provide a helpful answer in {selected_language}."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Error fetching answer."

if st.button(st.session_state.translated_ui.get("ask_ai_chef", "Ask AI Chef 🤖")):
    if not question:
        st.warning("⚠️ Please enter a question.")
    else:
        answer = ask_ai_chef(question)
        st.write("**👨‍🍳 AI Chef Says:**")
        st.info(answer)

# Shopping List Generator
st.sidebar.subheader("🛒 Shopping List Generator")
enable_shopping_list = st.sidebar.checkbox("Enable Shopping List")

def extract_ingredients():
    try:
        prompt = f"Extract ingredients from this recipe:\n\n{st.session_state.recipe_text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "No ingredients found."

if enable_shopping_list:
    ingredients_list = extract_ingredients()
    st.subheader("📝 Your Shopping List:")
    st.text_area("Editable Shopping List", value=ingredients_list, height=200)

# Smart Recipe Scaling
st.sidebar.subheader("🍽️ Smart Recipe Scaling")
servings = st.sidebar.slider("Select Number of Servings:", min_value=1, max_value=100, value=4, step=1)

def scale_recipe(servings):
    try:
        prompt = f"Adjust ingredient quantities in this recipe to serve {servings} people:\n\n{st.session_state.recipe_text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Unable to scale recipe."

if st.sidebar.button("🔄 Scale Recipe"):
    if not st.session_state.recipe_text:
        st.sidebar.warning("⚠️ Generate a recipe first!")
    else:
        scaled_recipe = scale_recipe(servings)
        st.subheader(f"📏 Scaled Recipe for {servings} Servings:")
        st.write(scaled_recipe)
