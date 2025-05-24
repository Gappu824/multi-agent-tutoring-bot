# multi_agent_tutor/agents/tutor_agent.py
from .base_agent import BaseAgent
from .math_agent import MathAgent
from .physics_agent import PhysicsAgent
import google.generativeai as genai # For direct model call if needed for classifier
from config import DEFAULT_GEMINI_MODEL # To use consistent model for classifier

class TutorAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_instruction=None) # Tutor agent itself might not need a system instruction for its core routing logic
        self.math_agent = MathAgent()
        self.physics_agent = PhysicsAgent()
        self.name = "Tutor Agent"
        # Initialize a separate model instance for classification if preferred, or use the base one carefully.
        # Using a specific model for classification can be more reliable.
        self.classifier_model = genai.GenerativeModel(DEFAULT_GEMINI_MODEL)


    def classify_intent_with_llm(self, query: str) -> str:
        """Classifies query to 'math', 'physics', or 'general' using LLM."""
        prompt = f"""
        Analyze the following student query and classify its primary subject focus.
        Return ONLY one of the following category names: 'math', 'physics', or 'general'.

        Student Query: "{query}"

        Category:
        """
        response_text = "general" # Default
        try:
            response = self.classifier_model.generate_content(prompt) # Direct call for classification
            response_text = response.text.strip().lower()
        except Exception as e:
            print(f"[{self.name} Classifier] Error during LLM call: {e}")
            # Fallback to keyword matching or default if LLM fails
            query_lower = query.lower()
            if any(kw in query_lower for kw in ["math", "algebra", "calculate", "equation", "solve", "number", "geometry", "integral", "derivative"]):
                return "math"
            if any(kw in query_lower for kw in ["physics", "force", "energy", "motion", "gravity", "light", "thermodynamics", "relativity", "quantum"]):
                return "physics"
            return "general"


        print(f"[{self.name} Classifier] Raw classification: '{response_text}' for query: '{query}'")

        if "math" in response_text:
            return "math"
        elif "physics" in response_text:
            return "physics"
        else:
            # If LLM returns something unexpected, try basic keyword check as a fallback
            query_lower = query.lower()
            if any(kw in query_lower for kw in ["math", "algebra", "calculate", "equation", "solve", "number", "geometry", "integral", "derivative"]):
                return "math"
            if any(kw in query_lower for kw in ["physics", "force", "energy", "motion", "gravity", "light", "thermodynamics", "relativity", "quantum"]):
                return "physics"
            return "general"

    def route_query(self, query: str) -> str:
        print(f"[{self.name}] Received query for routing: {query}")

        self.math_agent.clear_history()
        self.physics_agent.clear_history()
        # self.clear_history() # Tutor agent's own history might be useful for long convos

        subject = self.classify_intent_with_llm(query)
        print(f"[{self.name}] Classified query as: {subject}")

        response = ""
        if subject == "math":
            response = self.math_agent.handle_query(query)
        elif subject == "physics":
            response = self.physics_agent.handle_query(query)
        else:
            print(f"[{self.name}] Handling as general query.")
            general_prompt = (
                "You are a helpful general knowledge Tutor Agent. "
                "The query could not be specifically classified as math or physics, or it's a general question. "
                f"Please answer the following student query to the best of your ability: \"{query}\""
            )
            # Use the base class's generate_response for the TutorAgent itself
            # Ensure Tutor Agent uses its own context if it's conversational
            # For a simple non-conversational Tutor Agent general response:
            temp_model = genai.GenerativeModel(DEFAULT_GEMINI_MODEL) # Fresh model for general query
            response = temp_model.generate_content(general_prompt).text
        return response

if __name__ == "__main__":
    try:
        tutor = TutorAgent()
        print("\n--- Testing Math Query ---")
        print(f"Tutor Response: {tutor.route_query('Can you help me solve 2x + 5 = 11? And also, what is 10 times 3?')}")
        # ... (other print statements for testing) ...
        print("\n--- Testing Physics Query ---")
        physics_query_text = "What is Newton's second law and the value of the gravitational constant G?"
        print(f"Tutor Response: {tutor.route_query(physics_query_text)}")
        # ... (other print statements for testing) ...
    except Exception as e:
        print(f"Error in TutorAgent test: {e}")
        print("Ensure GEMINI_API_KEY is set in .env")