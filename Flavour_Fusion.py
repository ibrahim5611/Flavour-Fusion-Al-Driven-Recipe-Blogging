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
    "Abkhazian": "Abkhazian",
    "Afrikaans": "Afrikaans",
    "Akan": "Akan",
    "Albanian": "Albanian",
    "Algerian": "Algerian",
    "American": "American",
    "Amharic": "Amharic",
    "Andorran": "Andorran",
    "Angolan": "Angolan",
    "Antiguan": "Antiguan",
    "Arabic": "Arabic",
    "Argentinian": "Argentinian",
    "Armenian": "Armenian",
    "Australian": "Australian",
    "Austrian": "Austrian",
    "Avar": "Avar",
    "Azerbaijani": "Azerbaijani",
    "Bahamian": "Bahamian",
    "Bahraini": "Bahraini",
    "Bangladeshi": "Bangladeshi",
    "Barbadian": "Barbadian",
    "Bashkir": "Bashkir",
    "Basque": "Basque",
    "Belarusian": "Belarusian",
    "Belgian": "Belgian",
    "Belizean": "Belizean",
    "Beninese": "Beninese",
    "Bengali": "Bengali",
    "Bhutanese": "Bhutanese",
    "Bisaya": "Bisaya",
    "Bolivian": "Bolivian",
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
    "Chichewa": "Chichewa",
    "Chinese": "Chinese",
    "Chukchi": "Chukchi",
    "Chuukese": "Chuukese",
    "Comoran": "Comoran",
    "Comorian": "Comorian",
    "Congolese": "Congolese",
    "Croatian": "Croatian",
    "Czech": "Czech",
    "Danish": "Danish",
    "Dargin": "Dargin",
    "Dane": "Dane",
    "Dholuo": "Dholuo",
    "Djiboutian": "Djiboutian",
    "Dominican": "Dominican",
    "Dutch": "Dutch",
    "East Timorese": "East Timorese",
    "Ecuadorian": "Ecuadorian",
    "Egyptian": "Egyptian",
    "Emirati": "Emirati",
    "Enets": "Enets",
    "Eritrean": "Eritrean",
    "Equatorial Guinean": "Equatorial Guinean",
    "Erzya": "Erzya",
    "Estonian": "Estonian",
    "Ethiopian": "Ethiopian",
    "Even": "Even",
    "Evenki": "Evenki",
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
    "Hausa": "Hausa",
    "Hebrew": "Hebrew",
    "Hindi": "Hindi",
    "Hungarian": "Hungarian",
    "Icelandic": "Icelandic",
    "Igbo": "Igbo",
    "Indonesian": "Indonesian",
    "Ingrian": "Ingrian",
    "Ingush": "Ingush",
    "Ivorian": "Ivorian",
    "Italian": "Italian",
    "Itelmen": "Itelmen",
    "Japanese": "Japanese",
    "Javanese": "Javanese",
    "Kabardian": "Kabardian",
    "Kalenjin": "Kalenjin",
    "Kalmyk": "Kalmyk",
    "Kamba": "Kamba",
    "Kannada": "Kannada",
    "Karachay-Balkar": "Karachay-Balkar",
    "Karelian": "Karelian",
    "Kazakh": "Kazakh",
    "Khakas": "Khakas",
    "Khanty": "Khanty",
    "Khmer": "Khmer",
    "Kikongo": "Kikongo",
    "Kikuyu": "Kikuyu",
    "Kinyarwanda": "Kinyarwanda",
    "Kiribati": "Kiribati",
    "Kirundi": "Kirundi",
    "Kisii": "Kisii",
    "Kiswahili": "Kiswahili",
    "Kituba": "Kituba",
    "Komi": "Komi",
    "Korean": "Korean",
    "Koryak": "Koryak",
    "Kosovar": "Kosovar",
    "Kosraean": "Kosraean",
    "Kumyk": "Kumyk",
    "Kurdish": "Kurdish",
    "Kyrgyz": "Kyrgyz",
    "Lao": "Lao",
    "Latvian": "Latvian",
    "Lesothoan": "Lesothoan",
    "Lezgian": "Lezgian",
    "Liberian": "Liberian",
    "Lingala": "Lingala",
    "Lithuanian": "Lithuanian",
    "Luxembourgish": "Luxembourgish",
    "Luganda": "Luganda",
    "Macedonian": "Macedonian",
    "Madagascan": "Madagascan",
    "Malagasy": "Malagasy",
    "Malawian": "Malawian",
    "Malay": "Malay",
    "Malayalam": "Malayalam",
    "Malian": "Malian",
    "Maltese": "Maltese",
    "Maithili": "Maithili",
    "Maldivian": "Maldivian",
    "Maasai": "Maasai",
    "Marshallese": "Marshallese",
    "Mauritanian": "Mauritanian",
    "Mauritian": "Mauritian",
    "Mexican": "Mexican",
    "Moldovan": "Moldovan",
    "Mongolian": "Mongolian",
    "Montenegrin": "Montenegrin",
    "Mordvin": "Mordvin",
    "Mozambican": "Mozambican",
    "Nanai": "Nanai",
    "Namibian": "Namibian",
    "Nandi": "Nandi",
    "Nauruan": "Nauruan",
    "Nepali": "Nepali",
    "Nenets": "Nenets",
    "Nganasan": "Nganasan",
    "Nigerian": "Nigerian",
    "Nigerien": "Nigerien",
    "Norwegian": "Norwegian",
    "Odia": "Odia",
    "Oromo": "Oromo",
    "Ossetian": "Ossetian",
    "Palauan": "Palauan",
    "Papua New Guinean": "Papua New Guinean",
    "Pashto": "Pashto",
    "Persian": "Persian",
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
    "Somali": "Somali",
    "Spanish": "Spanish",
    "Sundanese": "Sundanese",
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
    "Tigrinya": "Tigrinya",
    "Togolese": "Togolese",
    "Tongan": "Tongan",
    "Turkish": "Turkish",
    "Turkmen": "Turkmen",
    "Tuvaluan": "Tuvaluan",
    "Tuvinian": "Tuvinian",
    "Udmurt": "Udmurt",
    "Ukrainian": "Ukrainian",
    "Urdu": "Urdu",
    "Uzbek": "Uzbek",
    "Vanuatuan": "Vanuatuan",
    "Vietnamese": "Vietnamese",
    "Wallisian": "Wallisian",
    "Welsh": "Welsh",
    "Xhosa": "Xhosa",
    "Yapese": "Yapese",
    "Yoruba": "Yoruba",
    "Zambian": "Zambian",
    "Zimbabwean": "Zimbabwean",
    "Zulu": "Zulu"
}

# Supported Cuisines
cuisines = [
    "None", "Italian", "Indian", "Mexican", "Chinese", "Thai", "French", "Mediterranean", "Japanese", "Korean", "Greek", "Spanish", "Middle Eastern", "American", "British", "German", "Brazilian", "Russian", "African", "Caribbean", "Vietnamese", "Turkish", "Moroccan", "Peruvian", "Filipino", "Indonesian", "Malaysian", "Australian", "Canadian", "Scandinavian", "Polish", "Portuguese", "Irish", "Scottish", "Dutch", "Belgian", "Swiss", "Austrian", "Hungarian", "Czech", "Slovak", "Romanian", "Bulgarian", "Ukrainian", "Georgian", "Armenian", "Lebanese", "Israeli", "Iranian", "Iraqi", "Egyptian", "Tunisian", "Algerian", "Nigerian", "Ethiopian", "Kenyan", "South African", "Ghanaian", "Ivorian", "Senegalese", "Cameroonian", "Angolan", "Mozambican", "Argentinian", "Chilean", "Colombian", "Venezuelan", "Ecuadorian", "Bolivian", "Paraguayan", "Uruguayan", "Costa Rican", "Panamanian", "Cuban", "Puerto Rican", "Dominican", "Haitian", "Jamaican", "Bahamian", "Trinidadian", "Guyanese", "Surinamese", "Fijian", "Tongan", "Samoan", "Papua New Guinean", "Solomon Islander", "New Zealand"
]

# Function to generate a joke dynamically using Gemini API in the selected language
def get_joke(language):
    """Generates a fresh, unique and funny joke in the selected language."""
    try:
        random_seed = random.randint(1, 100000)
        timestamp = int(time.time())

        prompt = f"Tell me a unique and funny joke in {language}. Make sure it's different from any previous joke. (Seed: {random_seed}, Time: {timestamp})"

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

# AI Cooking Assistant Chatbot
def chat_with_assistant(user_query):
    """Provides real-time cooking help, ingredient substitutes, and cooking tips."""
    try:
        response = model.generate_content(f"Answer this cooking-related question: {user_query}")
        return response.text.strip()
    except Exception as e:
        st.error(f"Error fetching assistant response: {e}")
        return "Sorry, I couldn't find an answer to your question."

# Streamlit UI
st.title("Flavour Fusion: AI-Driven Recipe Blogging")
st.subheader("Generate AI-powered recipes with customization, multi-language support, and cultural adaptations!")

# User Input Section
user_input = st.text_input("Enter a Recipe Topic (e.g., 'Vegan Chocolate Cake'):", "")
ingredients = st.text_area("Enter Ingredients (comma-separated):", "")
word_count = st.number_input("Enter Word Count:", min_value=100, max_value=2000, step=100, value=500)

# Customization Options
dietary_preference = st.selectbox("Select Dietary Preference:", ["None", "Vegan", "Vegetarian", "Non-Vegetarian", "Alcohol-Free","Gluten-Free", "Keto", "Paleo", "Halal", "Kosher", "Low-Carb", "Low-Fat", "Low-Sodium", "Nut-Free", "Sugar-Free", "Whole30", "Pescatarian", "Lactose-Free", "Dairy-Free", "Egg-Free", "Soy-Free", "Shellfish-Free","Peanut-Free", "Tree Nut-Free", "Wheat-Free", "Sesame-Free", "Mustard-Free", "Celery-Free", "Sulfite-Free", "Lupin-Free","Mollusk-Free"])
cooking_time = st.slider("Max Cooking Time (minutes):", min_value=5, max_value=120, value=30, step=5)
flavor_profile = st.selectbox("Select Flavor Profile:", ["None", "Spicy", "Sweet", "Savory", "Sour", "Umami", "Bitter", "Salty", "Mild", "Hot", "Cold", "Refreshing", "Rich", "Creamy", "Crunchy", "Soft", "Chewy", "Juicy", "Tangy", "Zesty", "Fruity", "Nutty", "Herbal", "Earthy", "Smoky", "Garlicky", "Citrusy", "Peppery", "Sour-Sweet", "Sour-Spicy", "Sweet-Spicy", "Sweet-Sour", "Savory-Sweet", "Savory-Spicy", "Savory-Sour", "Savory-Bitter", "Savory-Sweet-Spicy", "Savory-Sweet-Sour", "Savory-Sweet-Bitter", "Savory-Sweet-Spicy-Sour", "Savory-Sweet-Spicy-Bitter", "Savory-Sweet-Sour-Bitter", "Savory-Sweet-Spicy-Sour-Bitter"])

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

# AI Cooking Assistant Chatbot
st.sidebar.title("👨‍🍳 AI-Powered Cooking Assistant")
st.sidebar.write("Ask real-time cooking questions, get ingredient substitutes, and more!")

user_query = st.sidebar.text_input("Ask me anything about cooking:")
if user_query:
    assistant_response = chat_with_assistant(user_query)
    st.sidebar.write(f"**AI Cooking Assistant:** {assistant_response}")
