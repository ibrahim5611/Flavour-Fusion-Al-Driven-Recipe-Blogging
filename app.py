import streamlit as st
import google.generativeai as genai
import random
api_key = "AIzaSyBbNR2uwOZa9O-Qx60EEv2kyw5MTVusyFc"
genai.configure(api_key=api_key)
#configure the model generation settings
generation_config = {
    "temperature": 0.75,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 192,
    "response_mime_type": "text/plain",
}
zzzzzzzzzz
# Function to generate a joke
def get_joke():
    jokes = [
        "Why don't programmers like nature? It has too many bugs.",
        "Why do Java developers wear glasses? Because they don't see sharp.",
        "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
        "Why don't programmers like nature? It has too many bugs.",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why do Java developers wear glasses? Because they don't see sharp.",
        "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
        "Why do Python programmers prefer using snake_case? Because it's easier to read!",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "Why did the developer go broke? Because he used up all his cache.",
        "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25.",
        "Why did the programmer get kicked out of the beach? Because he kept using the 'C' language!",
        "Why was the computer cold? It left its Windows open."
    ]
    return random.choice (jokes)

def recepie_generation(user_input, word_count):
    """
    Function to generate a blog based on user input and word count.
    Parameters:
    user_input (str): The topic for the blog.
    word_count (int): The desired number of words for the blog.
    Returns:
    str: The generated blog content.
    """
    # Display a message while the blog is being generated
    st.write("### Generating your recepie...")
    st.write(f"While I work on creating your blog, here's a little joke to keep you entertained:\n\n**{get_joke()}**")
    # Start a chat session with the input topic and word count
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Write a recepie based on the input topic: {user_input} and number of words: {word_count}\n",
                ],
            },
        ]
    )
    try:
        # Generate a response for the new input
        response = chat_session.send_message(user_input)
        st.success(" Your recepie is ready!")
        return response.text
    except Exception as e:
        st.error (f"Error generating blog: {e}")
        return None