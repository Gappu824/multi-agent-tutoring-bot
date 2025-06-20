# Multi-Agent Tutoring Bot 🤖📚

A sophisticated AI-powered tutoring assistant that intelligently routes student queries to specialized agents for Math and Physics. Built with Python, FastAPI, and Google's Gemini API, and deployed on Railway.

## 📋 Overview

This project implements a multi-agent system where a main **Tutor Agent** acts as an orchestrator. It receives student queries, classifies their intent (Math, Physics, or General), and delegates them to the appropriate specialist agent. Specialist agents (Math Agent, Physics Agent) are equipped with tools (e.g., a calculator for the Math Agent, a constants lookup for the Physics Agent) to provide accurate and comprehensive answers. The system is designed based on principles similar to Google's Agent Development Kit (ADK) concepts.

## ✨ Features

* **Intelligent Query Routing:** The Tutor Agent uses the Gemini API to classify queries, ensuring they are handled by the most suitable specialist.
* **Specialist Agents:**
    * **Math Agent:** Handles mathematical questions and can use a `simple_calculator` tool for arithmetic operations.
    * **Physics Agent:** Addresses physics-related inquiries and can utilize a `get_physics_constant` tool to look up physical constants.
* **Tool Usage:** Sub-agents are prompted to request tool use via a specific JSON format when needed. The agent then parses this request, calls the appropriate Python tool function, and incorporates the tool's output into its final response generated by the Gemini API.
* **Gemini API Integration:** Powered by Google's Gemini models (`gemini-1.5-flash-latest` by default) for natural language understanding, classification, and response generation.
* **FastAPI Backend:** Exposes a robust and interactive API (with Swagger UI documentation) for interacting with the Tutor Agent.
* **Deployable:** Includes a `Dockerfile` for easy deployment on platforms like Railway.

## 🏛️ Architecture

The system follows a multi-agent architecture:

1.  **User Query:** A student submits a query via the `/ask` API endpoint.
2.  **Tutor Agent (Orchestrator):**
    * Receives the query.
    * Uses its `classify_intent_with_llm` method (powered by Gemini) to determine if the query's primary subject is Math, Physics, or General.
    * Routes the query to the corresponding specialist agent (`MathAgent` or `PhysicsAgent`).
    * If the query is classified as General, the Tutor Agent handles it directly using its own Gemini model instance.
3.  **Specialist Agents (MathAgent, PhysicsAgent):**
    * Each agent is initialized with a system instruction guiding its expertise and tool usage.
    * When handling a query, the agent first prompts the Gemini API. The LLM is instructed to output a specific JSON structure (`{"tool_name": "...", "tool_input": "..."}`) if it determines a tool is necessary.
    * The agent's Python code parses this JSON. If a valid tool request is found, the corresponding Python tool function (e.g., `simple_calculator` or `get_physics_constant`) is executed with the provided input.
    * The agent then formulates a final response by re-prompting its Gemini model with the original query context and the tool's output, instructing it to incorporate the information naturally.
4.  **Response to User:** The Tutor Agent returns the specialist agent's (or its own) formulated answer to the user via the API.

```
[User] --- (Query JSON) ---> [FastAPI POST /ask]
                                |
                                v
                          [Tutor Agent]
                         /    |    \
                        /     |     \  (Classify Intent using Gemini)
                       v      v      v
        [Math Agent]------>[Physics Agent]------>[Tutor Agent (General)]
           |  (Uses Gemini)    | (Uses Gemini)       (Uses Gemini)
           |                   |
  (Requests Calculator Tool) (Requests Constants Tool)
           |                   |
  [Calculator Tool]     [Constants Lookup Tool]
 (Python function)     (Python function)
```

**Note on Tool Usage:** The current implementation uses a string-parsing method where the LLM is prompted to output a JSON request for a tool. For production-grade systems, **Gemini's native Function Calling (Tool Use) feature is highly recommended** for more reliable and structured tool invocation.

## 🛠️ Tech Stack

* **Backend:** Python 3.9+
* **Framework:** FastAPI
* **LLM:** Google Gemini API (via `google-generativeai` SDK)
* **ASGI Server:** Uvicorn
* **Environment Management:** `python-dotenv`
* **Data Validation:** Pydantic
* **Deployment:** Docker, Railway

## 🚀 Getting Started

### Prerequisites

* Python 3.9 or higher.
* Anaconda or Miniconda (recommended for local environment management).
* Git.
* A Google Gemini API Key: Obtain from [ai.google.dev](https://ai.google.dev). **Keep this key secret!**
* Docker Desktop (optional, for local Docker builds/testing).

### 1. Clone the Repository

```bash
git clone [https://github.com/Gappu824/multi-agent-tutoring-bot.git](https://github.com/Gappu824/multi-agent-tutoring-bot.git)
cd multi-agent-tutoring-bot
```

### 2. Set Up Environment

**Using Anaconda (Recommended):**

```bash
# Create and activate a new conda environment
conda create -n tutor_bot_env python=3.9 -y
conda activate tutor_bot_env

# Install dependencies from requirements.txt
pip install -r requirements.txt
```

**Using `venv` (Standard Python):**

```bash
python -m venv venv
# Activate venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key for Local Development

* Create a file named `.env` in the project root directory (`multi_agent_tutor/.env`).
* Add your Gemini API Key to the `.env` file:

    ```env
    GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
    ```
    **(Remember to use your secured API key here. This file is listed in `.gitignore` and should NOT be committed to GitHub.)**

### 4. Run the Application Locally

Ensure your Conda environment (e.g., `tutor_bot_env`) or `venv` is activated.

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://127.0.0.1:8000`.
API documentation (Swagger UI) can be accessed at `http://127.0.0.1:8000/docs`.

## 🧪 API Endpoints

* `GET /`: Welcome message and links to documentation.
    * **Response:**
        ```json
        {
            "message": "Welcome to the Multi-Agent Tutoring Bot API!",
            "documentation": "/docs",
            "ask_endpoint": "/ask (POST)"
        }
        ```
* `POST /ask`: Submit a query to the Tutor Agent.
    * **Request Body (JSON):**
        ```json
        {
            "query": "Your question here, e.g., What is 2+2?"
        }
        ```
    * **Successful Response Body (JSON):**
        ```json
        {
            "answer": "The tutor bot's detailed answer to your query."
        }
        ```
    * **Error Response Body (JSON, e.g., for empty query):**
        ```json
        {
            "detail": "Query cannot be empty."
        }
        ```

## ☁️ Deployment

This application is deployed on **Railway** using Docker.

* **Repository:** `https://github.com/Gappu824/multi-agent-tutoring-bot`
* **Live Deployed Application URL:** `https://multi-agent-tutoring-bot-production-004b.up.railway.app` (Please verify this is the current active URL from your Railway dashboard)

### Deployment Steps for Railway:

1.  The project includes a `Dockerfile` that Railway uses to build and deploy the application.
2.  The `GEMINI_API_KEY` **must be set as an environment variable** in the Railway project/service settings (Variables tab). It should NOT be taken from a `.env` file in the deployed environment.
3.  Railway automatically detects pushes to the linked GitHub repository's `main` branch and triggers new deployments.

## 🌟 Bonus Points & Potential Enhancements

This project meets the core requirements. Potential areas for bonus points or future enhancements include:

* **Conversation History:** Implement context management within agents for follow-up questions.
* **More Specialist Agents:** Expand to subjects like Chemistry or History.
* **Advanced Tooling & Function Calling:** Migrate to Gemini's native Function Calling feature for more robust and structured tool invocation instead of JSON string parsing.
* **Enhanced UI:** Develop a simple web frontend (e.g., using Streamlit, or HTML/JS with Fetch API) to interact with the bot more easily than Postman/curl.
* **Streaming Responses:** Implement streaming for longer answers to improve perceived responsiveness.
* **More Sophisticated Error Handling:** Add more granular error handling within agents and tool usage.

## 📝 License

This project is open-source. (Consider adding a specific license like MIT if desired).
