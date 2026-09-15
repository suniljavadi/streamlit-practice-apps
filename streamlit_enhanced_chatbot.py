import streamlit as st
from textblob import TextBlob

try:
    from googletrans import Translator
except Exception:
    Translator = None

# Initialize the translator
translator = Translator() if Translator is not None else None

# Function to detect language
def detect_language(text):
    return TextBlob(text).detect_language()

# Function for sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Set up the Streamlit app
st.title("Enhanced Chatbot")
st.write("This is an enhanced chatbot with various features.")

# Language selection
language = st.selectbox("Select Language", ["English", "Spanish", "French", "German"])

# Text input
user_input = st.text_input("You: ")

if user_input:
    # Translate user input to English if not in English
    if language != "English" and translator is not None:
        try:
            user_input_translated = translator.translate(user_input, dest='en').text
        except Exception:
            user_input_translated = user_input
    else:
        user_input_translated = user_input

    # Analyze sentiment
    sentiment = analyze_sentiment(user_input_translated)

    # Generate a response (simple echo for demonstration)
    response = f"I understood you said: '{user_input_translated}'. Sentiment: {sentiment}."

    # Translate response back to selected language
    if language != "English" and translator is not None:
        try:
            response = translator.translate(response, dest=language.lower()).text
        except Exception:
            pass

    # Display the response
    st.write("Chatbot: ", response)

# File upload functionality
uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
if uploaded_file is not None:
    # Read and display the content of the uploaded file
    content = uploaded_file.read().decode("utf-8")
    st.write("File content:", content)

    # Respond based on file content (simple echo for demonstration)
    st.write("Chatbot: I received your file. You can ask me about its content.")
