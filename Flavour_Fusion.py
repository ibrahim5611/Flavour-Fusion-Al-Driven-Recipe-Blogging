import streamlit as st
import google.generativeai as genai
import os
import random
import time
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
import io

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

# Apply custom CSS for better styling
st.markdown("""
    <style>
        body {
            background-color: #f8f9fa;
        }
        .stButton>button {
            color: white;
            hover-color: white;
            background-color: #ff4b4b;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 18px;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            padding: 20px;
            font-size: 16px;
        }
        .stTitle {
            color: #ff4b4b;
            text-align: center;
        }
        .stSubheader {
            color: #ff4b4b;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Function to translate UI dynamically
def translate_text(text, target_language):
    try:
        prompt = f"Translate the following text into {target_language} in a only in one line : {text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return text  # Return original text if translation fails

# Function to update UI translations dynamically
def update_ui_language(selected_language):
    ui_texts = {
        "title": "Flavour Fusion: AI-Driven Recipe Blogging",
        "enter_recipe_details": "Enter Recipe Details",
        "select_language": "Select Language",
        "ai_generated_recipe": "AI-Generated Recipe:",
        "food_pairings": "Food Pairing Suggestions:",
        "ai_chef_q&a": "Live Q&A with AI Chef",
        "ask_question": "Ask a question about the recipe:",
        "ask_ai_chef": "Ask AI Chef",
        "enable_shopping_list": "Enable Shopping List",
        "smart_scaling": "Smart Recipe Scaling",
        "scale_recipe": "Scale Recipe",
        "your_shopping_list": "Your Shopping List",
        "export_pdf": "Export as PDF",
        "export_png": "Export as PNG",
        "export_jpg": "Export as JPG",
        "joke_of_the_day": "Joke of the day: ",
        "shopping_list_generator": "Shopping List Generator",
        "editable_shopping_list": "Editable Shopping List",
        "shopping_list": "Shopping List",
        "generate_recipe": "Generate Recipe",
        "dietary_preference": "Dietary Preference:",
        "apply_language": "Apply Language",
        "select_language": "Select Language",
        "settings": "Settings",
        "select_cuisine": "Select Cuisine:",
        "dietary_preference": "Dietary Preference:",
        "cooking_time": "Max Cooking Time (minutes):",
        "flavor_profile": "Flavor Profile:"
    }
    
    for key, value in ui_texts.items():
        st.session_state.translated_ui[key] = translate_text(value, selected_language)


# Sidebar for settings
st.sidebar.title(st.session_state.translated_ui.get("settings","Settings"))
selected_language = st.sidebar.text_input("Enter Language (e.g., Spanish, French, Hindi):", "English")
if st.sidebar.button(st.session_state.translated_ui.get("apply_language","Apply Language")):
    update_ui_language(selected_language)

cuisine = st.sidebar.selectbox(st.session_state.translated_ui.get("select_cuisine","Select Cuisine:"), ["Okay with any cuisine", "Italian", "Indian", "Mexican", "Chinese", "Thai", "French", "Mediterranean", "Japanese", "Korean", "Greek", "Spanish", "Middle Eastern", "American", "British", "German", "Brazilian", "Russian", "African", "Caribbean", "Vietnamese", "Turkish", "Moroccan", "Peruvian", "Filipino", "Indonesian", "Malaysian", "Australian", "Canadian", "Scandinavian", "Polish", "Portuguese", "Irish", "Scottish", "Dutch", "Belgian", "Swiss", "Austrian", "Hungarian", "Czech", "Slovak", "Romanian", "Bulgarian", "Ukrainian", "Georgian", "Armenian", "Lebanese", "Israeli", "Iranian", "Iraqi", "Egyptian", "Tunisian", "Algerian", "Nigerian", "Ethiopian", "Kenyan", "South African", "Ghanaian", "Ivorian", "Senegalese", "Cameroonian", "Angolan", "Mozambican", "Argentinian", "Chilean", "Colombian", "Venezuelan", "Ecuadorian", "Bolivian", "Paraguayan", "Uruguayan", "Costa Rican", "Panamanian", "Cuban", "Puerto Rican", "Dominican", "Haitian", "Jamaican", "Bahamian", "Trinidadian", "Guyanese", "Surinamese", "Fijian", "Tongan", "Samoan", "Papua New Guinean", "Solomon Islander", "New Zealander", "Vanuatuan"])
dietary_preference = st.sidebar.selectbox(st.session_state.translated_ui.get("dietary_preference","Dietary Preference:"), ["Okay with any dietary preference", "Vegan", "Vegetarian", "Non-Vegetarian", "Alcohol-Free","Gluten-Free", "Keto", "Paleo", "Halal", "Kosher", "Low-Carb", "Low-Fat", "Low-Sodium", "Nut-Free", "Sugar-Free", "Whole30", "Pescatarian", "Lactose-Free", "Dairy-Free", "Egg-Free", "Soy-Free", "Shellfish-Free","Peanut-Free", "Tree Nut-Free", "Wheat-Free", "Sesame-Free", "Mustard-Free", "Celery-Free", "Sulfite-Free", "Lupin-Free","Mollusk-Free"])
cooking_time = st.sidebar.slider(st.session_state.translated_ui.get("cooking_time","Max Cooking Time (minutes):"), min_value=5, max_value=120, value=30, step=5)
flavor_profile = st.sidebar.selectbox(st.session_state.translated_ui.get("flavor_profile","Flavor Profile:"), ["Not specified", "Spicy", "Sweet", "Savory", "Sour", "Umami", "Bitter", "Salty", "Mild", "Hot", "Cold", "Refreshing", "Rich", "Creamy", "Crunchy", "Soft", "Chewy", "Juicy", "Tangy", "Zesty", "Fruity", "Nutty", "Herbal", "Earthy", "Smoky", "Garlicky", "Citrusy", "Peppery"])


# User Input Section (Merged Recipe Name & Ingredients)
st.title(st.session_state.translated_ui.get("title", "Flavour Fusion: AI-Driven Recipe Blogging"))
st.subheader(st.session_state.translated_ui.get("enter_recipe_details", "Enter Recipe Details"))
recipe_details = st.text_area("Enter a recipe name, ingredients, or both:", "", height=100)
word_count = st.number_input("Enter Word Count:", min_value=100, max_value=3000, step=100, value=500)

# Function to generate a joke dynamically
def get_joke(selected_language):
    try:
        random_seed = random.randint(1, 10000)
        timestamp = int(time.time())
        prompt = f"Tell me a unique and funny joke in {selected_language}, you can say joke about any thing you want but it should have to be in {selected_language}. (Seed: {random_seed}, Time: {timestamp})"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return f"Oops! Couldn't fetch a joke in {selected_language} this time."

# Function to generate food pairing suggestions
def get_food_pairing(recipe_name, cuisine):
    try:
        prompt = f"Suggest complementary dishes, drinks, and desserts for {recipe_name} that match {cuisine} cuisine and It should be fully in the {selected_language}."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "No pairing suggestions available."

# Function to generate the recipe with merged input
def generate_recipe():
    if not recipe_details:
        st.warning("⚠️ Please enter a recipe name or ingredients!")
        return

    st.write(f"### Generating your {cuisine if cuisine != 'Okay with any cuisine' else ''} recipe in {selected_language}...")

    joke = get_joke(selected_language)
    st.info((st.session_state.translated_ui.get("joke_of_the_day","Joke of the day:")) + f"{joke}")

    # Construct prompt
    prompt = f"Write a {word_count}-word recipe based on the following details: {recipe_details}. Generate the recipe in {selected_language}."
    if dietary_preference:
        prompt += f" Ensure the recipe follows a {dietary_preference} diet."
    if cooking_time:
        prompt += f" The total cooking time should be under {cooking_time} minutes."
    if flavor_profile:
        prompt += f" Make the dish {flavor_profile} in taste."
    if cuisine != "None":
        prompt += f" Ensure the recipe follows {cuisine} cuisine traditions, including authentic ingredients and cooking methods."
    prompt += f" Also, provide a detailed nutritional breakdown in {selected_language}."

    try:
        response = model.generate_content(prompt)
        st.session_state.recipe_text = response.text.strip()
        st.session_state.food_pairings = get_food_pairing(recipe_details, cuisine)

    except Exception as e:
        st.error(f"Error generating recipe: {e}")

# Generate Button
if st.button(st.session_state.translated_ui.get("generate_recipe","Generate Recipe")):
    generate_recipe()


# Display stored recipe if available
if st.session_state.recipe_text:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(st.session_state.translated_ui.get("ai_generated_recipe", "AI-Generated Recipe:"))
        st.write(st.session_state.recipe_text)

    with col2:
        st.subheader(st.session_state.translated_ui.get("food_pairings", "Food Pairing Suggestions:"))
        st.write(st.session_state.food_pairings)

# Live Q&A Section
st.subheader(st.session_state.translated_ui.get("ai_chef_q&a", "Live Q&A with AI Chef"))
question = st.text_input(st.session_state.translated_ui.get("ask_a_question_about_the_recipe", "Ask a question about the recipe (e.g., 'What can I use instead of eggs?'):"))

# Function to answer cooking-related questions
def ask_ai_chef(question, recipe_text):
    """Answers user questions about the recipe using Gemini AI."""
    if not question:
        return "Please enter a question about the recipe."
    
    try:
        prompt = f"The following is a recipe: {recipe_text}. The user has a question: {question}. Provide a helpful and concise answer in {selected_language}."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error fetching answer: {e}"

# Answer Button
if st.button("Ask AI Chef"):
    if not question:
        st.warning("⚠️ Please enter a question.")
    else:
        answer = ask_ai_chef(question, st.session_state.recipe_text)  # Use stored recipe
        st.write("**👨‍🍳 AI Chef Says:**")
        st.info(answer)

# Add Shopping List Section in Sidebar
st.sidebar.subheader(st.session_state.translated_ui.get("shopping_list_generator", "Shopping List Generator"))
enable_shopping_list = st.sidebar.checkbox(st.session_state.translated_ui.get("enable_shopping_list", "Enable Shopping List"))

if enable_shopping_list:
    st.sidebar.success(st.session_state.translated_ui.get("enable_shopping_list", "Enable Shopping List"))

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

    st.subheader(st.session_state.translated_ui.get("your_shopping_list", "Your Shopping List",))
    st.text_area((st.session_state.translated_ui.get("editable_shopping_list", "Editable Shopping List")), value=st.session_state.shopping_list, height=200)

# Function to create a PDF shopping list
def create_pdf():
    """Creates and exports the shopping list as a PDF."""
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 750, "Shopping List")
    
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
    img = Image.new("RGB", (800, 800), "white")
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("NotoSans-Regular.ttf", 24)
    except:
        font = ImageFont.load_default()

    draw.text((50, 50), "Shopping List", fill="black", font=font)
    
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
        if st.button(st.session_state.translated_ui.get("export_pdf", "Export as PDF")):
            pdf_file = create_pdf()
            st.download_button(label="Download PDF", data=pdf_file, file_name="Shopping_List.pdf", mime="application/pdf")

    with col2:
        if st.button(st.session_state.translated_ui.get("export_png", "Export as PNG")):
            img_file = create_image()
            st.download_button(label="Download PNG", data=img_file, file_name="Shopping_List.png", mime="image/png")

    with col3:
        if st.button(st.session_state.translated_ui.get("export_jpg", "Export as JPG")):
            img_file = create_image()
            st.download_button(label="Download JPG", data=img_file, file_name="Shopping_List.jpg", mime="image/jpeg")


# Add Smart Recipe Scaling Section in Sidebar
st.sidebar.subheader(st.session_state.translated_ui.get("smart_scaling", "Smart Recipe Scaling"))
servings = st.sidebar.slider("Slide to select number of Servings:", min_value=1, max_value=100, value=4, step=1)

# Function to scale recipe ingredients based on servings
def scale_recipe(recipe_text, servings):
    """Scales recipe ingredient quantities based on servings."""
    try:
        prompt = f"Adjust the ingredient quantities in the following recipe to serve {servings} people, make sure it is fully given in {selected_language}:\n\n{recipe_text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Unable to scale the recipe at the moment."

# Button to scale recipe
if st.sidebar.button("Scale Recipe"):
    if not st.session_state.recipe_text:
        st.sidebar.warning("Generate a recipe first before scaling!")
    else:
        scaled_recipe = scale_recipe(st.session_state.recipe_text, servings)
        st.subheader(f"Scaled Recipe for {servings} Servings:")
        st.write(scaled_recipe)
        st.sidebar.success("Recipe scaled successfully!")