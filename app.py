import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import random

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

# Joke Generator Function
def get_joke():
    jokes = [
        "Why don't programmers like nature? It has too many bugs.",
        "Why do Java developers wear glasses? Because they don't see sharp.",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the developer go broke? Because he used up all his cache."
    ]
    return random.choice(jokes)

# Function to suggest a traditional or regional dish based on ingredients
def suggest_traditional_dish(ingredients):
    """Uses Gemini AI to find a traditional dish matching given ingredients."""
    prompt = f"Suggest a well-known traditional or regional dish that uses these ingredients: {ingredients}. Only return the dish name."
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error finding a traditional dish: {e}")
        return None

# Function to generate a recipe
def generate_recipe(user_input, word_count, ingredients="", matched_recipe=""):
    """Generates a recipe based on topic, ingredients, or matched traditional dish."""
    st.write("### 🍳 Generating your recipe...")
    st.write(f"While waiting, here's a joke: **{get_joke()}** 😂")

    # Construct prompt based on user choice
    if matched_recipe:
        prompt = f"Write a {word_count}-word recipe for {matched_recipe} using {ingredients}."
    elif ingredients:
        prompt = f"Write a {word_count}-word recipe using only these ingredients: {ingredients}."
    else:
        prompt = f"Write a {word_count}-word recipe on {user_input}."

    try:
        # Start a chat session with Gemini AI
        chat_session = model.start_chat(history=[
            {"role": "user", "parts": [prompt]},
        ])
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating recipe: {e}")
        return "Sorry, an error occurred!"

# Streamlit UI
st.title("Flavour Fusion: AI-Driven Recipe Blogging")
st.subheader("Generate AI-powered recipes and explore traditional dishes!")

# User Input Section
user_input = st.text_input("Enter a Recipe Topic (optional):", "")
ingredients = st.text_area("Enter Ingredients (comma-separated):", "")
word_count = st.number_input("Enter Word Count:", min_value=100, max_value=2000, step=100, value=500)

# Suggest Traditional Dish Button
if st.button("Find a Traditional Dish"):
    if ingredients:
        suggested_dish = suggest_traditional_dish(ingredients)
        if suggested_dish:
            st.write(f"### 🍽️ Suggested Dish: **{suggested_dish}**")
            st.write("Does this match what you were thinking?")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"✅ Yes, Generate {suggested_dish}"):
                    recipe = generate_recipe(user_input, word_count, ingredients, matched_recipe=suggested_dish)
                    st.write("## 🍽️ Your AI-Generated Recipe:")
                    st.write(recipe)
            
            with col2:
                if st.button("🔄 No, Find Another Dish"):
                    st.experimental_rerun()  # Refresh the app to find another dish
            
            with col3:
                if st.button("✨ No, Create My Own Recipe"):
                    recipe = generate_recipe(user_input, word_count, ingredients)
                    st.write("## 🍽️ Your AI-Generated Recipe:")
                    st.write(recipe)
        else:
            st.warning("Could not find a traditional dish for the given ingredients.")
    else:
        st.warning("Please enter ingredients first!")

# Generate AI Recipe Directly
if st.button("Generate AI Recipe"):
    if not user_input and not ingredients:
        st.warning("Please enter either a recipe topic or ingredients!")
    else:
        recipe = generate_recipe(user_input, word_count, ingredients)
        st.write("## 🍽️ Your AI-Generated Recipe:")
        st.write(recipe)
