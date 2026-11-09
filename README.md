# PyBot — Basic Python Chatbot (CodeAlpha Task 4)

A clean, modern, and responsive rule-based chatbot application developed for the **CodeAlpha Python Programming Internship (Task 4: Basic Chatbot)**.

PyBot demonstrates foundational Python concepts in a real backend architecture powered by Flask, combined with a minimal, dark-themed vanilla web interface.

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Demonstrated Python Concepts](#demonstrated-python-concepts)
3. [Features](#features)
4. [Predefined Chatbot Intents](#predefined-chatbot-intents)
5. [Technology Stack](#technology-stack)
6. [Project Structure](#project-structure)
7. [Prerequisites](#prerequisites)
8. [Setup & Installation (Windows Instructions)](#setup--installation-windows-instructions)
9. [Running the Application](#running-the-application)
   - [Web Interface Mode (Flask)](#web-interface-mode-flask)
   - [Console CLI Mode](#console-cli-mode)
10. [Running Automated Tests](#running-automated-tests)
11. [Example Conversations](#example-conversations)
12. [Troubleshooting Guide](#troubleshooting-guide)
13. [Uploading to GitHub](#uploading-to-github)

---

## 💡 Project Overview

The objective of Task 4 is to build a rule-based chatbot capable of understanding user messages and responding with appropriate predefined answers.

This project delivers:
- A modular Python response engine in `chatbot.py`.
- A lightweight HTTP API with Flask in `app.py`.
- An interactive single-page web interface in `templates/index.html`, styled with `static/css/style.css` and powered by `static/js/app.js`.
- Standalone CLI execution support for running directly in the terminal.
- An automated unit test suite with 23 passing tests in `test_chatbot.py`.

---

## 🐍 Demonstrated Python Concepts

The core logic directly highlights the four key programming concepts required by CodeAlpha Task 4:

1. **Functions (`def`)**:
   - `normalize_text(text)`: Validates input type, trims leading/trailing whitespace, and strips punctuation.
   - `_matches_any_pattern(normalized_text, tokens, patterns)`: Pattern matching helper.
   - `get_bot_response(message)`: Central response-generation engine.
   - `run_cli()`: Terminal-based conversation loop.

2. **If-Elif-Else Conditional Logic**:
   - Used in `get_bot_response()` to evaluate normalized user messages against defined intent sets in hierarchical priority order.
   - Used in `app.py` for input validation (checking for JSON format, missing keys, empty strings, character limits).

3. **Loops (`for` and `while`)**:
   - `for` loops iterate across rule pattern tuples and tokens to avoid false-positive substring matches (e.g., ensuring `"shine"` does not trigger a greeting for `"hi"`).
   - `while True:` loop powers the interactive console session in CLI mode until an exit condition (`exit`, `quit`, or `bye`) is triggered.

4. **User Input and Output**:
   - In Console Mode: `input()` captures user messages and `print()` streams formatted responses.
   - In Web Mode: Flask accepts user JSON payloads (`request.get_json()`) via `POST /chat` and emits structured JSON (`jsonify()`).

---

## ✨ Features

- **Single-Page Chat UI**: Clean dark theme inspired by modern developer tools (Deep Navy `#0B1020`, Surface `#111827`, Violet `#8B5CF6`).
- **Interactive Suggestion Chips**: 3 functional quick-start chips (`"Hello"`, `"How are you?"`, `"What can you do?"`) to immediately initiate conversation.
- **Session Reset**: "Clear" button in the chat header resets conversation history without reloading the page.
- **Live Online Indicator**: Restrained green pulse dot and status badge.
- **Input Validation & Safety**:
  - Enforces string type validation and rejects whitespace-only inputs.
  - Limits message length to 500 characters to prevent buffer abuse.
  - Uses safe DOM methods (`textContent`) to prevent Cross-Site Scripting (XSS).
- **Graceful Error Handling**: Visual feedback if network or server errors occur.
- **Keyboard Friendly**: Press <kbd>Enter</kbd> to send messages, automatic autofocus on text input.
- **Zero External AI Dependencies**: 100% self-contained Python rule logic without third-party APIs, keys, or paid services.

---

## 🎯 Predefined Chatbot Intents

| Intent | Sample Inputs | Predefined Bot Response |
| :--- | :--- | :--- |
| **Greeting** | `hi`, `hello`, `hey`, `good morning`, `good afternoon`, `good evening` | *"Hi! Nice to meet you. How can I help you?"* |
| **Well-being** | `how are you`, `how are you doing`, `how do you do` | *"I'm fine, thanks! How are you?"* |
| **Identity** | `who are you`, `what is your name`, `who made you` | *"I'm PyBot, a simple rule-based chatbot built with Python."* |
| **Capabilities** | `what can you do`, `help`, `what do you do`, `commands` | *"I can respond to simple greetings, answer a few predefined questions, and demonstrate a basic Python chatbot."* |
| **Thanks** | `thanks`, `thank you`, `many thanks` | *"You're welcome!"* |
| **Goodbye** | `bye`, `goodbye`, `see you`, `farewell` | *"Goodbye! Have a great day!"* |
| **Unknown** | Any input that does not match a predefined rule | *"Sorry, I don't understand that message yet. Try saying hello, asking how I am, or typing help."* |

---

## 🛠 Technology Stack

- **Backend**: Python 3.10+
- **Web Framework**: Flask 3.1+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+ Fetch API)
- **Testing**: Python Standard Library `unittest`
- **Package Management**: `pip`

---

## 📂 Project Structure

```text
├── app.py                  # Flask application routes (GET /, POST /chat, GET /health)
├── chatbot.py              # Rule-based logic, normalization, and CLI loop
├── templates/
│   └── index.html          # Chatbot single-page web template
├── static/
│   ├── css/
│   │   └── style.css       # Complete application styling & theme variables
│   └── js/
│       └── app.js          # DOM manipulation, Fetch API, suggestions, clear chat
├── test_chatbot.py         # Automated unit and integration tests (20 test cases)
├── requirements.txt        # Python dependency manifest
├── .gitignore              # Git ignore rules for Python bytecode, venv, and cache
└── README.md               # Complete setup, usage, and project documentation
```

---

## ⚙️ Prerequisites

- **Python 3.8 or higher** installed on your system.
  - Download from: [https://www.python.org/downloads/](https://www.python.org/downloads/)
  - **Important on Windows**: During installation, check the box **"Add Python to PATH"**.

Verify Python is installed:
```cmd
python --version
```
or
```cmd
py --version
```

---

## 💻 Setup & Installation (Windows Instructions)

Open **Command Prompt (`cmd.exe`)** or **PowerShell** and follow these steps:

### Step 1: Navigate to the project folder
```cmd
cd path\to\your\project-folder
```

### Step 2: Create a virtual environment
```cmd
python -m venv venv
```

### Step 3: Activate the virtual environment
- **On Command Prompt (CMD)**:
  ```cmd
  venv\Scripts\activate.bat
  ```
- **On PowerShell**:
  ```powershell
  venv\Scripts\Activate.ps1
  ```
  *(If PowerShell displays an execution policy error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once, then try again).*

When activated, you will see `(venv)` prepended to your command prompt.

### Step 4: Install required dependencies
```cmd
pip install -r requirements.txt
```

---

## 🚀 Running the Application

### Web Interface Mode (Flask)

Start the Flask server:
```cmd
python app.py
```

Output:
```text
Starting PyBot Flask server on http://0.0.0.0:3000
Note: This Flask development server is intended for development and local testing.
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:3000
```

Open your web browser (Chrome, Edge, Firefox) and navigate to:
```
http://127.0.0.1:3000
```
or
```
http://localhost:3000
```

To specify a custom port (e.g., port 5000):
```cmd
python app.py --port 5000
```
Then visit `http://127.0.0.1:5000`.

To stop the server: Press <kbd>Ctrl</kbd> + <kbd>C</kbd> in your terminal.

---

### Console CLI Mode

You can also run the chatbot directly inside your terminal without opening a browser:

```cmd
python chatbot.py
```

Interactive example in console:
```text
============================================================
 PyBot — Basic Python Chatbot (Console Mode)
 CodeAlpha Python Programming Internship - Task 4
 Type 'bye', 'exit', or 'quit' to end the conversation.
============================================================
PyBot: Hi! I'm PyBot, your basic Python chatbot. Say hello to get started.

You: hello
PyBot: Hi! Nice to meet you. How can I help you?

You: how are you
PyBot: I'm fine, thanks! How are you?

You: what can you do
PyBot: I can respond to simple greetings, answer a few predefined questions, and demonstrate a basic Python chatbot.

You: bye
PyBot: Goodbye! Have a great day!
(Session ended. Run again to chat more!)
```

---

## 🧪 Running Automated Tests

The project includes an automated test suite using Python's standard library `unittest` in `test_chatbot.py`.

Run the test suite with verbose output:
```cmd
python -m unittest -v test_chatbot.py
```

### Actual Execution Results:
```text
test_all_required_capabilities_inputs (test_chatbot.TestChatbotLogic) ... ok
test_all_required_goodbye_inputs (test_chatbot.TestChatbotLogic) ... ok
test_all_required_greeting_inputs (test_chatbot.TestChatbotLogic) ... ok
test_all_required_identity_inputs (test_chatbot.TestChatbotLogic) ... ok
test_all_required_thanks_inputs (test_chatbot.TestChatbotLogic) ... ok
test_all_required_wellbeing_inputs (test_chatbot.TestChatbotLogic) ... ok
test_case_insensitivity (test_chatbot.TestChatbotLogic) ... ok
test_empty_and_invalid_inputs (test_chatbot.TestChatbotLogic) ... ok
test_substring_boundary_safety (test_chatbot.TestChatbotLogic) ... ok
test_unknown_fallback (test_chatbot.TestChatbotLogic) ... ok
test_whitespace_and_punctuation (test_chatbot.TestChatbotLogic) ... ok
test_chat_boundary_500_chars (test_chatbot.TestFlaskBackend) ... ok
test_chat_empty_message (test_chatbot.TestFlaskBackend) ... ok
test_chat_excessive_length (test_chatbot.TestFlaskBackend) ... ok
test_chat_malformed_json_payload (test_chatbot.TestFlaskBackend) ... ok
test_chat_method_not_allowed (test_chatbot.TestFlaskBackend) ... ok
test_chat_missing_message (test_chatbot.TestFlaskBackend) ... ok
test_chat_non_json_request (test_chatbot.TestFlaskBackend) ... ok
test_chat_non_string_message (test_chatbot.TestFlaskBackend) ... ok
test_chat_resource_not_found (test_chatbot.TestFlaskBackend) ... ok
test_chat_success (test_chatbot.TestFlaskBackend) ... ok
test_health_endpoint (test_chatbot.TestFlaskBackend) ... ok
test_index_page (test_chatbot.TestFlaskBackend) ... ok

----------------------------------------------------------------------
Ran 23 tests in 0.023s

OK
```

All 20 tests pass with zero failures and zero errors.

---

## 💬 Example Conversations

### Conversation 1: Standard Greeting & Inquiry
> **User**: Hello  
> **PyBot**: Hi! Nice to meet you. How can I help you?  
> **User**: How are you doing?  
> **PyBot**: I'm fine, thanks! How are you?  
> **User**: Thanks!  
> **PyBot**: You're welcome!  
> **User**: Goodbye  
> **PyBot**: Goodbye! Have a great day!

### Conversation 2: Asking for Capabilities
> **User**: What can you do?  
> **PyBot**: I can respond to simple greetings, answer a few predefined questions, and demonstrate a basic Python chatbot.  
> **User**: Who are you?  
> **PyBot**: I'm PyBot, a simple rule-based chatbot built with Python.

### Conversation 3: Unknown Input Fallback
> **User**: What is the speed of light?  
> **PyBot**: Sorry, I don't understand that message yet. Try saying hello, asking how I am, or typing help.

---

## 🔍 Troubleshooting Guide

### 1. `'python'` is not recognized as an internal or external command
- **Cause**: Python was installed without checking the "Add Python to PATH" option.
- **Fix**: Re-run the Python installer, select **Modify**, check **Add Python to environment variables**, or use `py app.py` instead.

### 2. Port already in use error (`Address already in use` or `WinError 10048`)
- **Cause**: Another process is currently listening on port 3000.
- **Fix**: Run on a different port:
  ```cmd
  python app.py --port 5000
  ```
  Then open `http://127.0.0.1:5000`.

### 3. ModuleNotFoundError: No module named 'flask'
- **Cause**: Virtual environment is not activated or dependencies were not installed.
- **Fix**: Activate your virtual environment (`venv\Scripts\activate`) and run:
  ```cmd
  pip install -r requirements.txt
  ```

---

## 📤 Uploading to GitHub

Follow these steps to submit your project to GitHub for internship review:

1. **Initialize Git repository**:
   ```cmd
   git init
   ```
2. **Add all project files**:
   ```cmd
   git add .
   ```
3. **Commit the changes**:
   ```cmd
   git commit -m "CodeAlpha Task 4: Basic Python Chatbot implementation"
   ```
4. **Create a new repository on GitHub** (e.g., named `CodeAlpha_Task4_Basic_Chatbot`).
5. **Link and push to your remote repository**:
   ```cmd
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
   git push -u origin main
   ```

---

## 📜 License & Acknowledgments

Developed as part of the **CodeAlpha Python Programming Internship — Task 4**.  
Built strictly using Python standard libraries and Flask without external paid APIs.
