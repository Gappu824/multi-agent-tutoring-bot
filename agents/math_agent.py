# multi_agent_tutor/agents/math_agent.py
from .base_agent import BaseAgent
from .tools.calculator import simple_calculator
import re
import json

class MathAgent(BaseAgent):
    def __init__(self):
        system_instruction = (
            "You are the Math Agent, an expert in mathematics. "
            "Your primary goal is to help users understand and solve math problems. "
            "You have access to a 'calculator' tool. "
            "If a query involves arithmetic calculation that you should verify or perform, "
            "you MUST request to use the calculator by outputting a JSON object on a new line like this: "
            '```json\n{"tool_name": "calculator", "tool_input": "expression_string"}\n```. '
            "For example, to calculate 2+2, output: "
            '```json\n{"tool_name": "calculator", "tool_input": "2+2"}\n```. '
            "Do not perform calculations directly if they are suitable for the calculator; use the tool. "
            "Explain concepts clearly and provide step-by-step solutions when appropriate. "
            "After the tool provides a result, incorporate it naturally into your explanation."
        )
        super().__init__(system_instruction=system_instruction)
        self.tools = {"calculator": simple_calculator}
        self.name = "Math Agent"

    def handle_query(self, query: str) -> str:
        print(f"[{self.name}] Received query: {query}")

        initial_prompt = f"User query: \"{query}\"\nHow should I respond? If a calculation is needed, remember to request the calculator tool using the specified JSON format."
        llm_response_text = self.generate_response([initial_prompt])
        print(f"[{self.name}] LLM Initial Response Text: {llm_response_text}")

        tool_request_match = re.search(r"```json\s*(\{.*?\})\s*```", llm_response_text, re.DOTALL)

        if tool_request_match:
            try:
                tool_request_json = tool_request_match.group(1)
                tool_request = json.loads(tool_request_json)

                if tool_request.get("tool_name") == "calculator":
                    expression = tool_request.get("tool_input")
                    if expression:
                        print(f"[{self.name}] Attempting to use calculator for: {expression}")
                        calc_result = self.tools["calculator"](expression)
                        print(f"[{self.name}] Calculator result: {calc_result}")

                        tool_feedback_prompt = (
                            f"Okay, I've used the calculator for the expression '{expression}', and the result was '{calc_result}'.\n"
                            f"Now, formulate a comprehensive and helpful answer to the original user query: \"{query}\". "
                            "Incorporate the calculator's result smoothly into your explanation. Do not mention the JSON tool request format again."
                        )
                        # Provide some history for context if using chat-based generation
                        # For a simple one-shot with tool, you might construct a new prompt entirely.
                        # Here, we simulate a multi-turn like interaction.
                        contextual_prompt_parts = [
                            {"role": "user", "parts": [initial_prompt]}, # Original user query context
                            {"role": "model", "parts": [llm_response_text]}, # LLM's initial response (with tool request)
                            {"role": "user", "parts": [tool_feedback_prompt]} # Instruction with tool result
                        ]
                        # Temporarily clear history for this specific re-prompt if BaseAgent uses self.history for chat
                        original_history = self.history
                        self.history = [] # Start fresh for this re-prompt with full context
                        final_answer = self.generate_response(contextual_prompt_parts[2]["parts"]) # Send only the last user part for this specific re-prompt strategy
                        self.history = original_history # Restore

                        return final_answer
                    else:
                        return "Math Agent: I tried to use the calculator, but the expression was missing."
                else:
                    return f"Math Agent: I considered using a tool, but the request was not for the calculator. My response is: {llm_response_text.split('```json')[0].strip()}"

            except json.JSONDecodeError:
                print(f"[{self.name}] Failed to parse JSON tool request: {tool_request_match.group(1)}")
                return llm_response_text.split('```json')[0].strip()
            except Exception as e:
                print(f"[{self.name}] Error during tool processing: {e}")
                return "Math Agent: Sorry, an error occurred while trying to use my tools. Please try again."
        else:
            return llm_response_text

if __name__ == "__main__":
    try:
        agent = MathAgent()
        print("\n--- Testing Math Query with Calculation ---")
        print(agent.handle_query("What is 15 multiplied by 4, and then add 7 to the result?"))
        print("\n--- Testing Conceptual Math Query ---")
        print(agent.handle_query("Explain the Pythagorean theorem."))
    except Exception as e:
        print(f"Error in MathAgent test: {e}")
        print("Ensure GEMINI_API_KEY is set in .env")