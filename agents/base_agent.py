# multi_agent_tutor/agents/base_agent.py
import google.generativeai as genai
from config import GEMINI_API_KEY, DEFAULT_GEMINI_MODEL

# Configure the Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

class BaseAgent:
    def __init__(self, model_name=DEFAULT_GEMINI_MODEL, system_instruction=None):
        self.model_name = model_name
        # For newer Gemini models that support system instructions directly
        if system_instruction:
            self.model = genai.GenerativeModel(
                self.model_name,
                system_instruction=system_instruction
            )
        else:
            self.model = genai.GenerativeModel(self.model_name)

        self.history = [] # For potential conversation history (Bonus)

    def generate_response(self, prompt_parts, stream=False):
        """
        Generates a response from the Gemini model.
        Can handle single prompts or chat history.
        """
        try:
            # For chat-based interaction (maintains history):
            chat = self.model.start_chat(history=self.history)
            response = chat.send_message(prompt_parts)

            return response.text # For non-streaming

        except Exception as e:
            print(f"Error generating response with Gemini: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Gemini API Response Error: {e.response}")
                if hasattr(e.response, 'prompt_feedback') and e.response.prompt_feedback and hasattr(e.response.prompt_feedback, 'block_reason') and e.response.prompt_feedback.block_reason: # Check added
                    return f"Sorry, my response was blocked. Reason: {e.response.prompt_feedback.block_reason_message or e.response.prompt_feedback.block_reason}"
            return "Sorry, I encountered an error while trying to generate a response."

    def clear_history(self):
        self.history = []