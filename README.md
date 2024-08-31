# AI Business Assistant Chatbot

This repository contains a chatbot application designed to provide business assistance using OpenAI's API. The chatbot is implemented using Streamlit for the web interface and OpenAI's GPT model for natural language processing. The application allows users to interact with the chatbot, select different personas, and manage conversation history.

## Features

- **Chatbot Interface:** Users can interact with the chatbot via a web interface.
- **Personas:** Choose from predefined personas (Empathetic, Thoughtful, Strategic, Owner) or set a custom system message.
- **Conversation History:** Maintains conversation history, allowing you to reset or continue from past interactions.
- **Token Management:** Enforces a token budget to manage API usage.

## Prerequisites

- **Python 3.12 or newer**: The project uses the latest Python version.
- **Virtual Environment**: Recommended for managing dependencies.

## Installation

### Clone the Repository

```bash
git clone https://github.com/Huzaifaaazhar/AI-Business-Assistant-Bot.git
cd AI-Business-Assistant-Bot
```

### Set Up the Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv .venv
```

For Windows:

```bash
.\.venv\Scripts\activate
```

For macOS/Linux:

```bash
source .venv/bin/activate
```

### Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Configuration

### API Key

Create a `.env` file in the root directory of the project and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key
```

Ensure that the `.env` file is included in your `.gitignore` to prevent it from being committed to the repository.

### `.gitignore`

The `.gitignore` file should include:

```
.venv
.env
```

## Running the Application

To start the chatbot application, run:

```bash
streamlit run AI\ Virtual\ Assistant.py
```

### Web Interface

Once the application is running, open your web browser and navigate to `http://localhost:8501` to interact with the chatbot.

## Usage

1. **Choose a Persona:** Use the sidebar to select a persona or set a custom system message.
2. **Enter Your Message:** Type your message in the input box and press Enter.
3. **View Responses:** The chatbot will respond based on the selected persona and conversation history.

## Code Overview

### `AI Virtual Assistant.py`

- **Initialization:** Sets up the Streamlit interface and initializes the `BusinessBot` class.
- **Chat Management:** Handles user input, persona selection, and conversation history.
- **Display:** Renders the chat interface and displays messages.

### `BusinessBot` Class

- **Initialization:** Sets up API client, conversation history, and system messages.
- **Token Management:** Enforces a token budget and manages conversation history.
- **Chat Completion:** Interacts with OpenAI's API to generate responses.
- **History Management:** Loads, saves, and resets conversation history.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. Ensure that your contributions align with the project's goals and maintain code quality.

## Contact

For any questions or issues, please contact [Huzaifaaazhar](https://github.com/Huzaifaaazhar) or open an issue in the GitHub repository.
