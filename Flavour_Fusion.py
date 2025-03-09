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

# Apply custom CSS for better styling
st.markdown("""
    <style>
        body {
            background-color: #f8f9fa;
        }
        .stButton>button {
            color: white;
            background-color: #ff4b4b;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 18px;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            padding: 10px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for settings
st.sidebar.title("⚙️ Settings")
language = st.sidebar.selectbox("Select Language:", ["English", "Spanish", "French", "German", "Italian", "Hindi", "Chinese", "Japanese", "Arabic"])
cuisine = st.sidebar.selectbox("Select Cuisine:", ["None", "Italian", "Indian", "Mexican", "Chinese", "Thai", "French", "Mediterranean", "Japanese", "Korean"])
dietary_preference = st.sidebar.selectbox("Dietary Preference:", ["None", "Vegan", "Vegetarian", "Gluten-Free", "Keto", "Paleo", "Halal", "Kosher"])
cooking_time = st.sidebar.slider("Max Cooking Time (minutes):", min_value=5, max_value=120, value=30, step=5)
flavor_profile = st.sidebar.selectbox("Flavor Profile:", ["None", "Spicy", "Sweet", "Savory", "Sour", "Umami"])

# Main title
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>Flavour Fusion: AI Recipe Generator</h1>", unsafe_allow_html=True)

# User Input Section
st.subheader("🔍 Enter Your Recipe Preferences")
user_input = st.text_input("Recipe Name (e.g., 'Vegan Chocolate Cake'):", "")
ingredients = st.text_area("Enter Ingredients (comma-separated):", "")
word_count = st.number_input("Enter Word Count:", min_value=100, max_value=2000, step=100, value=500)

# Function to generate a joke dynamically
def get_joke(language):
    try:
        random_seed = random.randint(1, 10000)
        timestamp = int(time.time())
        prompt = f"Tell me a unique and funny programming joke in {language}. (Seed: {random_seed}, Time: {timestamp})"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return f"Oops! Couldn't fetch a joke in {language} this time."

# Function to generate food pairing suggestions
def get_food_pairing(recipe_name, cuisine):
    try:
        prompt = f"Suggest complementary dishes, drinks, and desserts for {recipe_name} that match {cuisine} cuisine."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "No pairing suggestions available."

# Store generated recipe in session state to prevent clearing
if "recipe_text" not in st.session_state:
    st.session_state.recipe_text = ""
if "food_pairings" not in st.session_state:
    st.session_state.food_pairings = ""

# Function to generate the recipe and store it
def generate_recipe():
    if not user_input and not ingredients:
        st.warning("⚠️ Please enter either a recipe topic or ingredients!")
        return

    st.write(f"### 🍳 Generating your {cuisine if cuisine != 'None' else ''} recipe in {language}...")

    joke = get_joke(language)
    st.info(f"💡 Joke of the day: {joke}")

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
    prompt += " Also, provide a detailed nutritional breakdown."

    try:
        response = model.generate_content(prompt)
        st.session_state.recipe_text = response.text.strip()  # Store in session state
        st.session_state.food_pairings = get_food_pairing(user_input, cuisine)

    except Exception as e:
        st.error(f"Error generating recipe: {e}")

# Generate Button
if st.button("Generate Recipe 🍽️"):
    generate_recipe()

# Display stored recipe if available
if st.session_state.recipe_text:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📜 AI-Generated Recipe:")
        st.write(st.session_state.recipe_text)

    with col2:
        st.subheader("🍷 Food Pairing Suggestions:")
        st.write(st.session_state.food_pairings)

# 🧑‍🍳 Live Q&A Section
st.subheader("🧑‍🍳 Live Q&A with AI Chef")
question = st.text_input("Ask a question about the recipe (e.g., 'What can I use instead of eggs?'):")

# Function to answer cooking-related questions
def ask_ai_chef(question, recipe_text):
    """Answers user questions about the recipe using Gemini AI."""
    if not question:
        return "Please enter a question about the recipe."
    
    try:
        prompt = f"The following is a recipe: {recipe_text}. The user has a question: {question}. Provide a helpful and concise answer."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error fetching answer: {e}"

# Answer Button
if st.button("Ask AI Chef 🤖"):
    if not question:
        st.warning("⚠️ Please enter a question.")
    else:
        answer = ask_ai_chef(question, st.session_state.recipe_text)  # Use stored recipe
        st.write("**👨‍🍳 AI Chef Says:**")
        st.info(answer)
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
import io

# Add Shopping List Section in Sidebar
st.sidebar.subheader("🛒 Shopping List Generator")
enable_shopping_list = st.sidebar.checkbox("Enable Shopping List")

# Function to extract ingredients as a list
def extract_ingredients(recipe_text):
    """Extracts ingredients from the recipe text."""
    try:
        prompt = f"Extract only the list of ingredients from the following recipe:\n\n{recipe_text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "No ingredients found."

# Function to generate a shopping list
def generate_shopping_list():
    """Generates a formatted shopping list from extracted ingredients."""
    if not st.session_state.recipe_text:
        st.warning("⚠️ Generate a recipe first to create a shopping list!")
        return
    
    ingredients_list = extract_ingredients(st.session_state.recipe_text)
    
    if "shopping_list" not in st.session_state:
        st.session_state.shopping_list = ingredients_list

    st.subheader("📝 Your Shopping List:")
    st.text_area("Editable Shopping List", value=st.session_state.shopping_list, height=200)

# Function to create a PDF shopping list
def create_pdf():
    """Creates and exports the shopping list as a PDF."""
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 750, "🛒 Shopping List")
    
    y_position = 730
    for line in st.session_state.shopping_list.split("\n"):
        pdf.drawString(100, y_position, f"- {line}")
        y_position -= 20
    
    pdf.save()
    buffer.seek(0)
    return buffer

# Function to create an image (PNG/JPG) of the shopping list
def create_image():
    """Creates an image of the shopping list."""
    img = Image.new("RGB", (600, 800), "white")
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    draw.text((50, 50), "🛒 Shopping List", fill="black", font=font)
    
    y_position = 100
    for line in st.session_state.shopping_list.split("\n"):
        draw.text((50, y_position), f"- {line}", fill="black", font=font)
        y_position += 30

    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    return img_buffer

# Export and Print Buttons
if enable_shopping_list:
    generate_shopping_list()

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export as PDF"):
            pdf_file = create_pdf()
            st.download_button(label="Download PDF", data=pdf_file, file_name="Shopping_List.pdf", mime="application/pdf")

    with col2:
        if st.button("🖼️ Export as PNG"):
            img_file = create_image()
            st.download_button(label="Download PNG", data=img_file, file_name="Shopping_List.png", mime="image/png")

    with col3:
        if st.button("🖼️ Export as JPG"):
            img_file = create_image()
            st.download_button(label="Download JPG", data=img_file, file_name="Shopping_List.jpg", mime="image/jpeg")

    # Print Button (Opens a new window for printing)
    st.markdown(
        "<script>function printShoppingList() { window.print(); }</script><button onclick='printShoppingList()'>🖨️ Print Shopping List</button>",
        unsafe_allow_html=True
    )
