# Multi-Agent Tutoring Bot 🤖📚

A sophisticated AI-powered tutoring assistant that intelligently routes student queries to specialized agents for Math and Physics. Built with Python, FastAPI, and Google's Gemini API.

## 📋 Overview

This project implements a multi-agent system where a main **Tutor Agent** acts as an orchestrator. It receives student queries, classifies their intent (Math, Physics, or General), and delegates them to the appropriate specialist agent. Specialist agents (Math Agent, Physics Agent) are equipped with tools (e.g., a calculator for the Math Agent, a constants lookup for the Physics Agent) to provide accurate and comprehensive answers. The system is designed based on principles similar to Google's Agent Development Kit (ADK) concepts.

## ✨ Features

* **Intelligent Query Routing:** Tutor Agent classifies queries to ensure they are handled by the most suitable specialist.
* **Specialist Agents:**
    * **Math Agent:** Handles mathematical questions, equipped with a `simple_calculator` tool.
    * **Physics Agent:** Addresses physics-related inquiries, utilizing a `get_physics_constant` tool.
* **Tool Usage:** Sub-agents can leverage tools to perform calculations or look up information, enhancing response accuracy.
* **Gemini API Integration:** Powered by Google's Gemini models for natural language understanding and generation.
* **FastAPI Backend:** Exposes a robust API for interaction.
* **Deployable:** Includes a Dockerfile for easy deployment on platforms like Railway or Vercel.

## 🏛️ Architecture

The system follows a multi-agent architecture:

1.  **User Query:** A student submits a query via the API.
2.  **Tutor Agent (Orchestrator):**
    * Receives the query.
    * Uses its LLM capabilities (Gemini) to classify the query's subject (Math, Physics, or General).
    * Routes the query to the corresponding specialist agent.
3.  **Specialist Agents (MathAgent, PhysicsAgent):**
    * Receive the query from the Tutor Agent.
    * Utilize their LLM capabilities (Gemini) and specific system prompts to understand and process the query.
    * **Tool Invocation:** If the query requires it (e.g., a calculation or a constant lookup), the agent's LLM is prompted to output a specific JSON structure requesting tool use. The agent's Python code parses this request, calls the appropriate Python tool function, and receives the result.
    * The agent then formulates a final response by re-prompting its LLM with the original query context and the tool's output.
4.  **Response to User:** The Tutor Agent returns the specialist agent's formulated answer to the user.

```
[User] --- Query ---> [FastAPI Endpoint]
                      |
                      v
                [Tutor Agent] -- Classify & Route --> [Math Agent] -- Uses --> [Calculator Tool]
                      |                                    |
                      `-- Classify & Route --> [Physics Agent] - Uses --> [Constants Tool]
                      |                                    |
                      `-- Handles General Query Directly   |
                                                         |
                      <--- Response <--------------------'
```

**Note on Tool Usage:** The current implementation uses a string-parsing method where the LLM is prompted to output a JSON request for a tool. For production-grade systems, **Gemini's native Function Calling (Tool Use) feature is highly recommended** for more reliable and structured tool invocation.

## 🛠️ Tech Stack

* **Backend:** Python 3.9+
* **Framework:** FastAPI
* **LLM:** Google Gemini API (via `google-generativeai` SDK)
* **Tools & Libraries:** Uvicorn, python-dotenv, Pydantic
* **Deployment:** Docker (for Railway, Vercel, etc.)

## 🚀 Getting Started

### Prerequisites

* Python 3.9 or higher.
* Anaconda or Miniconda (for easy environment management, optional but recommended for local dev).
* Git.
* A Google Gemini API Key: Obtain from [ai.google.dev](https://ai.google.dev). **Keep this key secret!**

### 1. Clone the Repository

```bash
git clone [https://github.com/Gappu824/multi-agent-tutoring-bot.git](https://github.com/Gappu824/multi-agent-tutoring-bot.git)
cd multi-agent-tutoring-bot
```

### 2. Set Up Environment

**Using Anaconda (Recommended for Local Development):**

```bash
# Create and activate a new conda environment
conda create -n tutor_bot_env python=3.9 -y
conda activate tutor_bot_env

# Install dependencies
pip install -r requirements.txt
```

**Using `venv` (Standard Python):**

```bash
python -m venv venv
# Activate venv
# Windows:
# venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

* Rename `.env.example` to `.env`.
* Open the `.env` file and add your **actual and secured** Gemini API Key:

    ```env
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```
    **(Remember to use your new, secured API key here and keep this `.env` file private).**

### 4. Run the Application Locally

Ensure your Conda environment (e.g., `tutor_bot_env`) or `venv` is activated.

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://127.0.0.1:8000`.
API documentation (Swagger UI) can be accessed at `http://120.0.0.1:8000/docs`.

## 🧪 API Endpoints

* `GET /`: Welcome message.
* `POST /ask`: Submit a query to the Tutor Agent.
    * **Request Body (JSON):**
        ```json
        {
            "query": "Your question here"
        }
        ```
    * **Response Body (JSON):**
        ```json
        {
            "answer": "The tutor bot's answer"
        }
        ```

## ☁️ Deployment

This application is designed to be deployed using Docker.

### Using Docker (General Steps for platforms like Railway)

1.  **Build the Docker Image (Optional - platforms often build from Dockerfile):**
    ```bash
    docker build -t multi-agent-tutor .
    ```

### Deployment to Railway / Vercel

* Push your code to your GitHub repository: `https://github.com/Gappu824/multi-agent-tutoring-bot.git`
* **Railway:**
    * Connect your GitHub repository to a new Railway project.
    * Railway should detect the `Dockerfile` and build/deploy automatically.
    * Add your `GEMINI_API_KEY` as an environment variable in the Railway project settings.
* **Vercel:**
    * Connect your GitHub repository to a new Vercel project.
    * Vercel can deploy Python applications using a `Dockerfile` or by detecting a `requirements.txt` and an ASGI entry point.
    * Add `GEMINI_API_KEY` as an environment variable in Vercel project settings.

**Live Deployed Application URL:** YOUR_DEPLOYED_APP_URL_HERE (You will get this after successful deployment)

## 🌟 Bonus Points & Potential Enhancements

* **Conversation History:** Implement context management for follow-up questions.
* **More Specialist Agents:** Add agents for other subjects.
* **Advanced Tooling:** Implement Gemini Function Calling.
* **Polished User Interface:** Develop a simple web frontend.
* **Advanced Error Handling & Input Validation.**

## 📜 License

This project is open-source. (Consider adding a specific license like MIT).