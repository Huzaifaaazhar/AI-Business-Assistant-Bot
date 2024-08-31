# Import necessary libraries
import os
import json
import openai
import tiktoken
import datetime as dt
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Define a class for the BusinessBot
class BusinessBot:
    def __init__(self, api_key, history_file=None, default_model="gpt-3.5-turbo",
                 default_temperature=0.2, default_max_tokens=200, token_budget=4096):
        # Initialize OpenAI client with the provided API key
        self.client = openai.OpenAI(api_key=api_key)

        # Set the history file to save conversation history
        if history_file is None:
            timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.history_file = f"conversation_history_{timestamp}.json"
        else:
            self.history_file = history_file
        
        # Initialize default settings
        self.default_model = default_model
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        self.token_budget = token_budget
        
        # Define different system personas for the chatbot
        self.system_messages = {
            "empathetic_assistant": "You're an assistant who provides empathetic responses to user's queries about business and startups",
            "thoughtful_assistant": "You're a thoughtful assistant who is always ready to dig deeper and provide detailed responses",
            "strategic_assistant": "You provide strategic answers to user's queries",
            "owner_assistant": "You're an assistant who provides business solution answers as an owner of a business would provide",
            "custom": "Enter your custom system message here:",
        }
        self.system_message = self.system_messages["thoughtful_assistant"]  # Default assistant
        self.load_conversation_history()  # Load conversation history from file

    # Method to count the number of tokens in a text
    def count_tokens(self, text):
        try:
            encoding = tiktoken.encoding_for_model(self.default_model)
        except KeyError:
            print(f"Warning: Model {self.default_model} not found. Using 'gpt-3.5-turbo' encoding as default.")
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            
        tokens = encoding.encode(text)
        return len(tokens)
    
    # Method to calculate total tokens used in conversation history
    def total_tokens_used(self):
        try:
            return sum(self.count_tokens(message['content']) for message in self.conversation_history)
        except Exception as e:
            print(f"An Unexpected error while calculating the total tokens: {e}")
            return None
    
    # Method to enforce the token budget by trimming conversation history
    def enforce_token_budget(self):
        try:
            while self.total_tokens_used() > self.token_budget:
                if len(self.conversation_history) <= 1:
                    break
                self.conversation_history.pop(1)
        except Exception as e:
            print(f"An Unexpected error while enforcing the token budget: {e}")

    # Method to set the persona for the chatbot
    def set_persona(self, persona):
        if persona in self.system_messages:
            self.system_message = self.system_messages[persona]
            self.update_system_message_in_history()
        else:
            raise ValueError(f"Unknown persona: {persona}. Available personas: {list(self.system_messages.keys())}")

    # Method to set a custom system message for the chatbot
    def set_custom_system_message(self, custom_message):
        if not custom_message:
            raise ValueError("Custom messages can't be empty")
        self.system_messages['custom'] = custom_message
        self.set_persona('custom')

    # Method to update the system message in the conversation history
    def update_system_message_in_history(self):
        try:
            if self.conversation_history and self.conversation_history[0]["role"] == "system":
                self.conversation_history[0]["content"] = self.system_message
            else:
                self.conversation_history.insert(0, {"role": "system", "content": self.system_message})
        except Exception as e:
            print(f"An Unexpected error while updating the system messages in convo history: {e}")

    # Method to generate a response using OpenAI's Chat API
    def chat_completion(self, prompt, temperature=None, max_tokens=None, model=None):
        temperature = temperature if temperature is not None else self.default_temperature
        max_tokens = max_tokens if max_tokens is not None else self.default_max_tokens
        model = model if model is not None else self.default_model

        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": prompt})

        # Enforce the token budget before generating a response
        self.enforce_token_budget()

        try:
            response = self.client.ChatCompletion.create(
                model=model,
                messages=self.conversation_history,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception as e:
            print(f"Error while generating response: {e}")
            return None
        
        AI_response = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": AI_response})
        self.save_conversation_history()
        return AI_response

    # Method to load conversation history from a file
    def load_conversation_history(self):
        try:
            with open(self.history_file, "r") as file:
                self.conversation_history = json.load(file)
        except FileNotFoundError:
            self.conversation_history = [{"role": "system", "content": self.system_message}]
        except json.JSONDecodeError:
            print("Error while reading the conversation file, starting with no history.")
            self.conversation_history = [{"role": "system", "content": self.system_message}]

    # Method to save conversation history to a file
    def save_conversation_history(self):
        try:
            with open(self.history_file, "w") as file:
                json.dump(self.conversation_history, file, indent=4)
        except IOError as e:
            print(f"An I/O error occurred while saving the conversation history: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while saving the conversation history: {e}")

    # Method to reset conversation history
    def reset_conversation_history(self):
        self.conversation_history = [{"role": "system", "content": self.system_message}]
        try:
            self.save_conversation_history()
        except Exception as e:
            print(f"An unexpected error occurred while resetting the conversation history: {e}")

# Streamlit UI setup
st.image("G://AI ChatBot//Neurals.jpg")
st.title("""AI Based Business Assistant :robot_face:""")

st.sidebar.header("Options")

# Initialize the chat manager in session state if not already present
if 'chat_manager' not in st.session_state:
    st.session_state["chat_manager"] = BusinessBot(api_key)

chat_manager = st.session_state["chat_manager"]

# Set up sliders for adjusting parameters
max_tokens_per_message = st.sidebar.slider("Max tokens per message", min_value=20, max_value=500, value=50)
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.01)

# Select system message persona
system_message = st.sidebar.selectbox("System Message", ["Empathetic", "Thoughtful", "Strategic", "Owner", "Custom"])

# Apply selected system message persona
if system_message == 'Empathetic':
    chat_manager.set_persona('empathetic_assistant')
elif system_message == 'Thoughtful':
    chat_manager.set_persona('thoughtful_assistant')
elif system_message == 'Strategic':
    chat_manager.set_persona('strategic_assistant')
elif system_message == 'Owner':
    chat_manager.set_persona('owner_assistant')
if system_message == 'Custom':
    custom_message = st.sidebar.text_area("Custom Message")
    if st.sidebar.button("Set Custom Message"):
        chat_manager.set_custom_system_message(custom_message)

# Button to reset conversation history
if st.sidebar.button("Reset Conversation History"):
    chat_manager.reset_conversation_history()
    st.session_state['conversation_history'] = chat_manager.conversation_history

# Initialize conversation history in session state if not already present
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = chat_manager.conversation_history

conversation_history = st.session_state['conversation_history']

# User input
user_input = st.chat_input("Write your message here")

# Generate response and add to conversation history if user input is provided
if user_input:
    response = chat_manager.chat_completion(user_input,
                                            temperature=temperature,
                                            max_tokens=max_tokens_per_message)

# Display conversation history
for message in conversation_history:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])
