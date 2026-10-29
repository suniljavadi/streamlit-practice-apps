# chatbot_app_advanced.py

import streamlit as st
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import random
import string
import time
from practice_utils import MAX_CHAT_MESSAGES, format_chat_export

try:
    import spacy
except Exception:
    spacy = None

try:
    from googletrans import Translator
except Exception:
    Translator = None

try:
    nlp = spacy.load("en_core_web_sm") if spacy is not None else None
except Exception:
    nlp = None

# Initialize the translator
translator = Translator() if Translator is not None else None

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Expanded conversation corpus
corpus = [
    "Hello, how are you?",
    "Hi, I am doing great! How can I assist you today?",
    "What's your name?",
    "My name is Chatbot. I'm here to help you.",
    "How can you help me?",
    "I can assist you with simple questions, tell jokes, or provide information about data science.",
    "What is data science?",
    "Data science is an interdisciplinary field that uses scientific methods to extract knowledge from data.",
    "Tell me a joke.",
    "Why don't scientists trust atoms? Because they make up everything!",
    "Goodbye!",
    "Bye! Have a great day!",
    "What can you do?",
    "I can chat with you, answer your questions, and tell you jokes.",
    "Who created you?",
    "I was created by an enthusiastic developer using Python and Streamlit!",
    "Thank you!",
    "You're welcome! Let me know if you need anything else."
]

# FAQs and their answers
faq = {
    "what is your name": "My name is Chatbot. I'm here to assist you.",
    "who created you": "I was created by an enthusiastic developer using Python and Streamlit.",
    "what can you do": "I can chat with you, answer questions, and make jokes.",
    "what is data science": "Data science is an interdisciplinary field that uses scientific methods to extract knowledge from data."
}

# Greetings and goodbye responses
greetings = ["Hello!", "Hi there!", "Hey!", "Greetings!", "Howdy!"]
goodbyes = ["Goodbye!", "See you later!", "Take care!", "Bye!", "Talk to you soon!"]

# Preprocess text function
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = ''.join([char for char in text if char not in string.punctuation])  # Remove punctuation
    try:
        tokens = word_tokenize(text)
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
    except LookupError:
        tokens = text.split()
    return ' '.join(tokens)

# Named Entity Recognition (NER) Function
def recognize_entities(user_input):
    if nlp is None:
        return []
    doc = nlp(user_input)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# FAQ and keyword recognition function
def check_faq(user_input):
    for question, answer in faq.items():
        if question in user_input.lower():
            return answer
    return None

# Function to detect the user's topic (simple keyword-based)
def detect_topic(user_input):
    topics = {
        "technology": ["python", "ai", "machine learning", "data science", "coding", "tech"],
        "sports": ["football", "cricket", "basketball", "tennis", "soccer", "sports"],
        "food": ["pizza", "burger", "sushi", "food", "dining"],
    }
    
    for topic, keywords in topics.items():
        if any(keyword in user_input.lower() for keyword in keywords):
            return topic
    return "general"

# Function to analyze user mood based on sentiment
def detect_user_mood(user_input):
    analysis = TextBlob(user_input)
    if analysis.sentiment.polarity > 0.5:
        return "happy"
    elif analysis.sentiment.polarity < -0.5:
        return "frustrated"
    else:
        return "neutral"

# Function to handle conversation context
def handle_context(user_input, previous_responses, mode):
    # Check if it's a FAQ
    faq_response = check_faq(user_input)
    if faq_response:
        return faq_response
    
    if 'what is your name' in user_input.lower():
        return "My name is Chatbot, nice to meet you!"
    if 'goodbye' in user_input.lower() or 'bye' in user_input.lower():
        return random.choice(goodbyes)
    
    if user_input.lower() in previous_responses:
        return "We've already discussed that. Any new questions?"
    
    return switch_personality(mode, user_input)

# Generate response based on user input
def generate_response(user_input, corpus):
    temp_corpus = corpus + [user_input]
    vectorizer = TfidfVectorizer(tokenizer=preprocess_text, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(temp_corpus)
    similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    idx = similarity.argsort()[0][-1]
    score = similarity[0][idx]
    threshold = 0.1
    
    if score < threshold:
        response = "I am sorry, I didn't understand that. Can you please rephrase?"
    else:
        response = corpus[idx]
    
    return response

# Function to handle feedback collection
def collect_feedback():
    st.write("Please provide feedback for this conversation:")
    rating = st.slider("Rate your experience (1-5)", 1, 5, 3)
    st.text_area("Any additional comments? (Not saved)")
    if st.button("Submit Feedback"):
        st.success(f"Thanks for your {rating}/5 feedback. It was not saved.")

# Function to translate text to a selected language
def translate_text(user_input, target_language):
    if translator is None:
        return user_input
    try:
        translation = translator.translate(user_input, dest=target_language)
        return translation.text
    except Exception:
        return user_input

# Initialize Streamlit app
def main():
    st.set_page_config(page_title="Advanced Chatbot", page_icon="🤖")
    st.title("🤖 Advanced Chatbot with Personalized Features")
    st.write("Hello! I'm your chatbot. Feel free to ask me anything.")
    
    # Initialize session state for conversation memory and mode
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    if 'previous_responses' not in st.session_state:
        st.session_state['previous_responses'] = []
    if 'mode' not in st.session_state:
        st.session_state['mode'] = 'informative'  # Default mode
    if 'user_name' not in st.session_state:
        st.session_state['user_name'] = None  # Store user's name
    if 'language' not in st.session_state:
        st.session_state['language'] = 'en'  # Default language
    
    # Ask for user's name if not already provided
    if st.session_state['user_name'] is None:
        st.session_state['user_name'] = st.text_input("What's your name?", key="name_input")
        if st.session_state['user_name']:
            st.write(f"Nice to meet you, {st.session_state['user_name']}!")

    # Select translation language
    language_options = ['en', 'fr', 'es', 'de', 'zh-cn', 'hi']
    st.session_state['language'] = st.selectbox("Select language for chatbot responses:", language_options)
    
    # User input
    user_input = st.text_input(
        f"{st.session_state['user_name']} (You): ",
        key="user_input",
        max_chars=2000,
    )

    # Mode selection
    mode = st.selectbox("Choose bot's personality", ["informative", "humorous", "casual"])

    # Display chat history
    chat_container = st.container()
    user_avatar = "👤"
    bot_avatar = "🤖"

    if st.button("Send"):
        if user_input:
            # Append user message to the conversation
            st.session_state['messages'].append({"role": "user", "content": user_input, "avatar": user_avatar})
            
            # Recognize entities
            entities = recognize_entities(user_input)
            if entities:
                st.session_state['messages'].append({"role": "bot", "content": f"I noticed you mentioned these entities: {entities}", "avatar": bot_avatar})

            # Detect user mood
            user_mood = detect_user_mood(user_input)
            if user_mood == "happy":
                st.session_state['messages'].append({"role": "bot", "content": "I'm glad to hear you're feeling happy!", "avatar": bot_avatar})
            elif user_mood == "frustrated":
                st.session_state['messages'].append({"role": "bot", "content": "I'm sorry you're feeling frustrated. How can I help?", "avatar": bot_avatar})

            # Handle topic detection
            topic = detect_topic(user_input)
            st.session_state['messages'].append({"role": "bot", "content": f"Looks like you're interested in {topic}. Let's talk more about that!", "avatar": bot_avatar})

            # Translate text if needed
            if st.session_state['language'] != 'en':
                translated_text = translate_text(user_input, st.session_state['language'])
                st.session_state['messages'].append({"role": "bot", "content": translated_text, "avatar": bot_avatar})

            # Get response from the bot
            response = handle_context(user_input, st.session_state['previous_responses'], mode)
            st.session_state['messages'].append({"role": "bot", "content": response, "avatar": bot_avatar})

            # Append to previous responses
            st.session_state['previous_responses'].append(user_input.lower())
            st.session_state['messages'] = st.session_state['messages'][-MAX_CHAT_MESSAGES:]
            st.session_state['previous_responses'] = st.session_state['previous_responses'][-MAX_CHAT_MESSAGES:]

    # Display chat history
    with chat_container:
        for message in st.session_state['messages']:
            st.markdown(f"**{message['avatar']} {message['role']}**: {message['content']}")

    st.download_button(
        "Download this chat",
        data=format_chat_export(st.session_state['messages']),
        file_name="chat-history.txt",
        mime="text/plain",
        disabled=not st.session_state['messages'],
    )
    if st.button("Clear chat"):
        st.session_state['messages'] = []
        st.session_state['previous_responses'] = []
        st.rerun()

    # Collect feedback
    collect_feedback()

if __name__ == "__main__":
    main()
