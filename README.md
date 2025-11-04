# 🤖 Streamlit Chatbot powered by Gemini

This guide explains what the Streamlit Chatbot application is, how to set up your development environment, and the critical steps for acquiring and securely setting your Google Gemini API key.

## 🌟 What is the App?

The Streamlit Chatbot (schatbot) is a sophisticated conversational application built with Python. It leverages the simplicity and speed of the **Streamlit** framework for its user interface while relying on the advanced capabilities of the **Google Gemini API** for intelligence and language generation.

Key features include:

* **Conversational Memory**: The chatbot remembers previous turns in the conversation, allowing for context-aware follow-up questions.
* **Intuitive UI**: A clean, single-page chat interface that is easy to use.
* **Powered by Gemini**: Uses Google's state-of-the-art Generative AI models (like gemini-2.5-flash) for fast and relevant responses.

## 🚀 Full Setup and Run Guide (Step-by-Step)

Follow these detailed steps to get the Streamlit Chatbot running on your local machine.

### Step 1: Clone the Project and Install Python Libraries

You will need **Python (3.9+)** and the **git** tool installed on your computer.

**1.1 Open your Terminal or Command Prompt**

Open your Terminal (Mac/Linux) or Command Prompt/PowerShell (Windows).

**1.2 Clone the project**

Download the code to your computer by running this command:

```bash
git clone https://github.com/Ashutosh-Jarag/schatbot.git
cd schatbot
```

**1.3 Create a Virtual Environment (Crucial for managing dependencies)**

This isolates the project's required packages:

```bash
python -m venv venv
```

**1.4 Activate the Virtual Environment**

On Mac/Linux:
```bash
source venv/bin/activate
```

On Windows (Command Prompt):
```bash
.\venv\Scripts\activate
```

**1.5 Install Required Libraries**

Install all necessary Python packages (Streamlit, Google GenAI SDK, etc.):

```bash
pip install -r requirements.txt
```

### Step 2: Get and Set Up Your Gemini API Key (Security Essential)

The API key is like a password that gives your application access to Google's AI models. It must be kept secret.

#### 🔑 How to Get Your Gemini API Key

1. **Visit the API Key Creation Page**: Go to the [official Google AI Studio API Key page](https://aistudio.google.com/app/apikey).
2. **Sign In**: Use your Google account to log in.
3. **Generate the Key**: Click the "Create API key" button.
4. **Copy and Secure**: Immediately copy the entire unique key string that appears. This is the only time you will see the full key, so copy it now.

#### ⚙️ Where to Set the API Key (The .env file)

**2.1 Create the .env file**

In the `schatbot/` directory (where your `app.py` or main Python script is), create a new file named exactly `.env` (start with a dot).

**2.2 Edit the File**

Open the newly created `.env` file using a text editor (like VS Code, Sublime Text, or Notepad) and paste your key using the variable name `GEMINI_API_KEY`:

```
GEMINI_API_KEY="PASTE_YOUR_COPIED_API_KEY_HERE"
```

**2.3 Security Note**

The code will automatically load the key from this file. Never commit the `.env` file to GitHub.

### Step 3: Launch the Chatbot Application

Once your virtual environment is active (from Step 1) and your API key is saved (from Step 2), you can run the app.

**3.1 Run the application**

```bash
# This command starts the Streamlit server
streamlit run app.py
```

**3.2 Access the App**

Your default web browser will automatically open the chatbot interface, usually at `http://localhost:8501`. You are now ready to start chatting!
