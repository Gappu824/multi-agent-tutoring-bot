# multi_agent_tutor/agents/physics_agent.py
from .base_agent import BaseAgent
from .tools.physics_constants import get_physics_constant
import re
import json

class PhysicsAgent(BaseAgent):
    def __init__(self):
        system_instruction = (
            "You are the Physics Agent, an expert in physics. "
            "Your primary goal is to help users understand physics concepts and problems. "
            "You have access to a 'get_physics_constant' tool. "
            "If a query requires information about a specific physical constant, "
            "you MUST request to use the tool by outputting a JSON object on a new line like this: "
            '```json\n{"tool_name": "get_physics_constant", "tool_input": "constant_name"}\n```. '
            "For example, to get the speed of light, output: "
            '```json\n{"tool_name": "get_physics_constant", "tool_input": "speed of light"}\n```. '
            "Do not guess constants; use the tool. "
            "Explain concepts clearly. "
            "After the tool provides data, incorporate it naturally into your explanation."
        )
        super().__init__(system_instruction=system_instruction)
        self.tools = {"get_physics_constant": get_physics_constant}
        self.name = "Physics Agent"

    def handle_query(self, query: str) -> str:
        print(f"[{self.name}] Received query: {query}")

        initial_prompt = f"User query: \"{query}\"\nHow should I respond? If a physical constant is needed, remember to request the 'get_physics_constant' tool using the specified JSON format."
        llm_response_text = self.generate_response([initial_prompt])
        print(f"[{self.name}] LLM Initial Response Text: {llm_response_text}")

        tool_request_match = re.search(r"```json\s*(\{.*?\})\s*```", llm_response_text, re.DOTALL)

        if tool_request_match:
            try:
                tool_request_json = tool_request_match.group(1)
                tool_request = json.loads(tool_request_json)

                if tool_request.get("tool_name") == "get_physics_constant":
                    constant_name = tool_request.get("tool_input")
                    if constant_name:
                        print(f"[{self.name}] Attempting to look up constant: {constant_name}")
                        constant_data_str = self.tools["get_physics_constant"](constant_name)
                        print(f"[{self.name}] Constant lookup result (raw): {constant_data_str}")

                        try:
                            constant_data = json.loads(constant_data_str)
                            if "error" in constant_data:
                                info_str = f"The constant '{constant_name}' could not be found or resulted in an error: {constant_data['error']}."
                            else:
                                info_str = f"The constant '{constant_name}' has a value of {constant_data.get('value')} {constant_data.get('unit', '')} (symbol: {constant_data.get('symbol', 'N/A')})."
                        except json.JSONDecodeError:
                             info_str = f"The tool returned malformed data for '{constant_name}': {constant_data_str}"

                        tool_feedback_prompt = (
                            f"Okay, I've used the 'get_physics_constant' tool for '{constant_name}', and the information found was: '{info_str}'.\n"
                            f"Now, formulate a comprehensive and helpful answer to the original user query: \"{query}\". "
                            "Incorporate this information smoothly into your explanation. Do not mention the JSON tool request format again."
                        )
                        contextual_prompt_parts = [
                            {"role": "user", "parts": [initial_prompt]},
                            {"role": "model", "parts": [llm_response_text]},
                            {"role": "user", "parts": [tool_feedback_prompt]}
                        ]
                        original_history = self.history
                        self.history = []
                        final_answer = self.generate_response(contextual_prompt_parts[2]["parts"])
                        self.history = original_history
                        return final_answer
                    else:
                         return "Physics Agent: I tried to look up a constant, but its name was missing."
                else:
                    return f"Physics Agent: I considered using a tool, but the request was not for 'get_physics_constant'. My response is: {llm_response_text.split('```json')[0].strip()}"

            except json.JSONDecodeError:
                print(f"[{self.name}] Failed to parse JSON tool request: {tool_request_match.group(1)}")
                return llm_response_text.split('```json')[0].strip()
            except Exception as e:
                print(f"[{self.name}] Error during tool processing: {e}")
                return "Physics Agent: Sorry, an error occurred while trying to use my tools. Please try again."
        else:
            return llm_response_text

if __name__ == "__main__":
    try:
        agent = PhysicsAgent()
        print("\n--- Testing Physics Query with Constant Lookup ---")
        print(agent.handle_query("What is Newton's second law? Also, speed of light value?"))
        print("\n--- Testing Conceptual Physics Query ---")
        print(agent.handle_query("Explain black holes."))
    except Exception as e:
        print(f"Error in PhysicsAgent test: {e}")
        print("Ensure GEMINI_API_KEY is set in .env")