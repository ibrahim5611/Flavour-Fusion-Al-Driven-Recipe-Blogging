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

# Supported Languages
languages = {
    "English": "English",
    "Spanish": "Spanish",
    "French": "French",
    "German": "German",
    "Italian": "Italian",
    "Hindi": "Hindi",
    "Chinese": "Chinese",
    "Japanese": "Japanese",
    "Arabic": "Arabic"
}

# Supported Cuisines
cuisines = [
    "None", "Italian", "Indian", "Mexican", "Chinese", "Thai", "French", "Mediterranean", "Japanese", "Korean"
]

# Function to generate a joke dynamically using Gemini API in the selected language
def get_joke(language):
    """Generates a fresh, unique programming-related joke in the selected language."""
    try:
        random_seed = random.randint(1, 10000)
        timestamp = int(time.time())

        prompt = f"Tell me a unique and funny programming joke in {language}. Make sure it's different from any previous joke. (Seed: {random_seed}, Time: {timestamp})"

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating joke: {e}")
        return f"Oops! Couldn't fetch a joke in {language} this time."

# Recipe & Customization Generator
def generate_recipe(user_input, word_count, ingredients="", dietary_preference="", cooking_time="", flavor_profile="", language="English", cuisine="None"):
    """Generates a recipe in the selected language and cuisine based on user preferences."""
    st.write(f"### 🍳 Generating your {cuisine if cuisine != 'None' else ''} recipe in {language}...")

    joke = get_joke(language)
    if joke:
        st.write(f"While waiting, here's a joke in {language}: **{joke}** 😂")

    # Construct prompt
    prompt = f"Write a {word_count}-word recipe on {user_input} in {language}."
    if ingredients:
        prompt += f" Use only the following ingredients: {ingredients}."
    if dietary_preference:
        prompt += f" Ensure the recipe follows a {dietary_preference} diet."
    if cooking_time:
        prompt += f" The total cooking time should be under {cooking_time} minutes."
    if flavor_profile:
        prompt += f" Make the dish {flavor_profile} in taste."
    if cuisine != "None":
        prompt += f" Ensure the recipe follows {cuisine} cuisine traditions, including authentic ingredients and cooking methods."

    # Request Nutritional Information
    prompt += " Also, provide a detailed nutritional breakdown for each ingredient used, including total calories, proteins, fats, and carbs."

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating recipe: {e}")
        return f"Sorry, an error occurred while generating the {cuisine} recipe in {language}."

# Streamlit UI
st.title("Flavour Fusion: AI-Driven Recipe Blogging")
st.subheader("Generate AI-powered recipes with customization, multi-language support, and cultural adaptations!")

# User Input Section
user_input = st.text_input("Enter a Recipe Topic (e.g., 'Vegan Chocolate Cake'):", "")
ingredients = st.text_area("Enter Ingredients (comma-separated):", "")
word_count = st.number_input("Enter Word Count:", min_value=100, max_value=2000, step=100, value=500)

# Customization Options
dietary_preference = st.selectbox("Select Dietary Preference:", ["None", "Vegan", "Vegetarian", "Gluten-Free", "Keto", "Paleo", "Halal", "Kosher"])
cooking_time = st.slider("Max Cooking Time (minutes):", min_value=5, max_value=120, value=30, step=5)
flavor_profile = st.selectbox("Select Flavor Profile:", ["None", "Spicy", "Sweet", "Savory", "Sour", "Umami"])

# Language Selection
language = st.selectbox("Select Language:", list(languages.keys()))

# Cuisine Selection
cuisine = st.selectbox("Select Cuisine:", cuisines)

# Generate Button
if st.button("Generate Recipe"):
    if not user_input and not ingredients:
        st.warning("Please enter either a recipe topic or ingredients!")
    else:
        recipe = generate_recipe(user_input, word_count, ingredients, dietary_preference, cooking_time, flavor_profile, language, cuisine)
        st.write(f"## 🍽️ Your {cuisine if cuisine != 'None' else ''} AI-Generated Recipe in {language}:")
        st.write(recipe)
