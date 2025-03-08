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
    "Albanian": "Albanian",
    "Angolan": "Angolan",
    "Arabic": "Arabic",
    "Armenian": "Armenian",
    "Azerbaijani": "Azerbaijani",
    "Bangladeshi": "Bangladeshi",
    "Basque": "Basque",
    "Balochi": "Balochi",
    "Belarusian": "Belarusian",
    "Belgian": "Belgian",
    "Bengali": "Bengali",
    "Bhutanese": "Bhutanese",
    "Bosnian": "Bosnian",
    "Botswanan": "Botswanan",
    "Bulgarian": "Bulgarian",
    "Burmese": "Burmese",
    "Cambodian": "Cambodian",
    "Cameroonian": "Cameroonian",
    "Cape Verdean": "Cape Verdean",
    "Carolinian": "Carolinian",
    "Central African": "Central African",
    "Chamorro": "Chamorro",
    "Chechen": "Chechen",
    "Chinese": "Chinese",
    "Chuukese": "Chuukese",
    "Comoran": "Comoran",
    "Comorian": "Comorian",
    "Congolese": "Congolese",
    "Croatian": "Croatian",
    "Czech": "Czech",
    "Dane": "Dane",
    "Danish": "Danish",
    "Djiboutian": "Djiboutian",
    "Dominican": "Dominican",
    "Dutch": "Dutch",
    "East Timorese": "East Timorese",
    "Ecuadorian": "Ecuadorian",
    "Egyptian": "Egyptian",
    "Emirati": "Emirati",
    "Equatorial Guinean": "Equatorial Guinean",
    "Eritrean": "Eritrean",
    "Estonian": "Estonian",
    "Ethiopian": "Ethiopian",
    "Faroese": "Faroese",
    "Fijian": "Fijian",
    "Filipino": "Filipino",
    "Finnish": "Finnish",
    "French": "French",
    "Futunan": "Futunan",
    "Georgian": "Georgian",
    "German": "German",
    "Ghanaian": "Ghanaian",
    "Greek": "Greek",
    "Greenlandic": "Greenlandic",
    "Gujarati": "Gujarati",
    "Hebrew": "Hebrew",
    "Hindi": "Hindi",
    "Hungarian": "Hungarian",
    "Icelandic": "Icelandic",
    "Indonesian": "Indonesian",
    "Ivorian": "Ivorian",
    "Italian": "Italian",
    "Japanese": "Japanese",
    "Kannada": "Kannada",
    "Kazakh": "Kazakh",
    "Khmer": "Khmer",
    "Kiribati": "Kiribati",
    "Korean": "Korean",
    "Kosovar": "Kosovar",
    "Kosraean": "Kosraean",
    "Kurdish": "Kurdish",
    "Kyrgyz": "Kyrgyz",
    "Lao": "Lao",
    "Latvian": "Latvian",
    "Lesothoan": "Lesothoan",
    "Liberian": "Liberian",
    "Lithuanian": "Lithuanian",
    "Luxembourgish": "Luxembourgish",
    "Macedonian": "Macedonian",
    "Madagascan": "Madagascan",
    "Malagasy": "Malagasy",
    "Malawian": "Malawian",
    "Malay": "Malay",
    "Malian": "Malian",
    "Maltese": "Maltese",
    "Maithili": "Maithili",
    "Maldivian": "Maldivian",
    "Marshallese": "Marshallese",
    "Mauritanian": "Mauritanian",
    "Mauritian": "Mauritian",
    "Mexican": "Mexican",
    "Moldovan": "Moldovan",
    "Mongolian": "Mongolian",
    "Montenegrin": "Montenegrin",
    "Mozambican": "Mozambican",
    "Namibian": "Namibian",
    "Nauruan": "Nauruan",
    "Nepali": "Nepali",
    "Nigerian": "Nigerian",
    "Nigerien": "Nigerien",
    "Norwegian": "Norwegian",
    "Odia": "Odia",
    "Palauan": "Palauan",
    "Pashto": "Pashto",
    "Polish": "Polish",
    "Portuguese": "Portuguese",
    "Punjabi": "Punjabi",
    "Pohnpeian": "Pohnpeian",
    "Romanian": "Romanian",
    "Russian": "Russian",
    "Samoan": "Samoan",
    "São Toméan": "São Toméan",
    "Serbian": "Serbian",
    "Seychellois": "Seychellois",
    "Sierra Leonean": "Sierra Leonean",
    "Sindhi": "Sindhi",
    "Sinhala": "Sinhala",
    "Slovak": "Slovak",
    "Slovenian": "Slovenian",
    "Solomon Islander": "Solomon Islander",
    "Spanish": "Spanish",
    "Swahili": "Swahili",
    "Swazi": "Swazi",
    "Swedish": "Swedish",
    "Swiss": "Swiss",
    "Tagalog": "Tagalog",
    "Tajik": "Tajik",
    "Tamil": "Tamil",
    "Tatar": "Tatar",
    "Telugu": "Telugu",
    "Thai": "Thai",
    "Tibetan": "Tibetan",
    "Togolese": "Togolese",
    "Tongan": "Tongan",
    "Turkish": "Turkish",
    "Turkmen": "Turkmen",
    "Tuvaluan": "Tuvaluan",
    "Ukrainian": "Ukrainian",
    "Urdu": "Urdu",
    "Uzbek": "Uzbek",
    "Vanuatuan": "Vanuatuan",
    "Vietnamese": "Vietnamese",
    "Wallisian": "Wallisian",
    "Yapese": "Yapese",
    "Zimbabwean": "Zimbabwean"
}

# Function to generate a joke dynamically using Gemini API in the selected language
def get_joke(language):
    """Generates a fresh, unique programming-related joke in the selected language."""
    try:
        random_seed = random.randint(1, 10000)
        timestamp = int(time.time())

        prompt = f"Tell me a random and funny joke in {language}. Make sure it's different from any previous jokes. (Seed: {random_seed}, Time: {timestamp})"

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating joke: {e}")
        return f"Oops! Couldn't fetch a joke in {language} this time."

# Recipe & Customization Generator
def generate_recipe(user_input, word_count, ingredients="", dietary_preference="", cooking_time="", flavor_profile="", language="English"):
    """Generates a recipe in the selected language based on user preferences and provides nutritional info."""
    st.write(f"### 🍳 Generating your recipe in {language}...")

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
    
    # Request Nutritional Information
    prompt += " Also, provide a detailed nutritional breakdown for each ingredient used, including total calories, proteins, fats, and carbs."

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating recipe: {e}")
        return f"Sorry, an error occurred while generating the recipe in {language}."

# Streamlit UI
st.title("Flavour Fusion: AI-Driven Recipe Blogging")
st.subheader("Generate AI-powered recipes with customization, multi-language support, and dynamic jokes!")

# User Input Section
user_input = st.text_input("Enter a Recipe Topic (e.g., 'Vegan Chocolate Cake'):", "")
ingredients = st.text_area("Enter Ingredients (comma-separated):", "")
word_count = st.number_input("Enter Word Count:", min_value=100, max_value=2000, step=100, value=500)

# Customization Options
dietary_preference = st.selectbox("Select Dietary Preference:", ["None", "Vegan", "Vegetarian", "Gluten-Free", "Keto", "Paleo", "Halal", "Kosher", "Low-Carb", "Low-Fat", "Low-Sodium", "Dairy-Free", "Nut-Free", "Sugar-Free", "Egg-Free", "Soy-Free", "Fish-Free", "Shellfish-Free", "Peanut-Free", "Tree Nut-Free", "Wheat-Free", "Sesame-Free", "Celery-Free", "Mustard-Free", "Sulfite-Free", "Lupin-Free", "Mollusk-Free", "Alcohol-Free", "No Restrictions", "Custom"])
cooking_time = st.slider("Max Cooking Time (minutes):", min_value=5, max_value=120, value=30, step=5)
flavor_profile = st.selectbox("Select Flavor Profile:", ["None", "Spicy", "Sweet", "Savory", "Sour", "Umami", "Bitter", "Salty", "Herbal", "Fruity", "Nutty", "Creamy", "Smoky", "Tangy", "Earthy", "Citrusy",  "Minty", "Floral", "Woody", "Gamey", "Rich", "Light", "Hearty", "Refreshing", "Zesty", "Robust", "Delicate", "Bold", "Mild", "Complex", "Simple", "Exotic", "Traditional", "Modern", "Fusion", "Regional", "Global", "Seasonal", "Local", "Organic", "Healthy", "Decadent", "Comforting", "Wholesome", "Indulgent", "Quick", "Easy", "Gourmet", "Budget-Friendly", "Kid-Friendly", "Party", "Holiday", "Celebration", "Weeknight", "Weekend", "Picnic", "BBQ", "Grilled", "Baked", "Fried", "Steamed", "Boiled", "Roasted", "Gravy", "Sauce", "Soup", "Salad", "Stew", "Curry", "Stir-Fry", "Bake", "Fry", "Grill", "Steam", "Boil", "Roast", "Simmer", "Sauté", "Broil", "Poach", "Braise", "Marinate", "Glaze", "Dip", "Spread", "Dress", "Garnish", "Season", "Spice", "Herb", "Condiment", "Appetizer", "Main Course", "Side Dish", "Dessert", "Snack", "Beverage", "Cocktail", "Mocktail", "Smoothie", "Shake", "Juice", "Soda", "Tea", "Coffee", "Milk", "Water", "Alcohol", "Wine", "Beer", "Spirits", "Liqueur", "Cider", "Champagne", "Mock Beer", "Mock Wine", "Mock Spirits", "Mock Liqueur", "Mock Cider", "Mock Champagne", "Mocktail Beer", "Mocktail Wine", "Mocktail Spirits", "Mocktail Liqueur", "Mocktail Cider", "Mocktail Champagne", "Mocktail", "Non-Alcoholic", "Low-Alcohol", "High-Alcohol", "Strong", "Light", "Medium", "Dry", "Sweet", "Semi-Sweet", "Semi-Dry", "Extra-Dry", "Extra-Sweet", "Extra-Spicy", "Extra-Savory", "Extra-Sour", "Extra-Umami", "Extra-Bitter", "Extra-Salty", "Extra-Herbal", "Extra-Fruity", "Extra-Nutty",])
# Language Selection
language = st.selectbox("Select Language:", list(languages.keys()))

# Generate Button
if st.button("Generate Recipe"):
    if not user_input and not ingredients:
        st.warning("Please enter either a recipe topic or ingredients!")
    else:
        recipe = generate_recipe(user_input, word_count, ingredients, dietary_preference, cooking_time, flavor_profile, language)
        st.write(f"## 🍽️ Your AI-Generated Recipe in {language}:")
        st.write(recipe)
