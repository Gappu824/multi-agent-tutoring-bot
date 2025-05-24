# multi_agent_tutor/agents/tools/physics_constants.py
import json

CONSTANTS = {
    "speed of light": {"value": 299792458, "unit": "m/s", "symbol": "c"},
    "gravitational constant": {"value": 6.67430e-11, "unit": "N(m/kg)^2", "symbol": "G"},
    "planck constant": {"value": 6.62607015e-34, "unit": "Js", "symbol": "h"},
    "boltzmann constant": {"value": 1.380649e-23, "unit": "J/K", "symbol": "k"},
    "electron mass": {"value": 9.1093837015e-31, "unit": "kg", "symbol": "m_e"},
    "proton mass": {"value": 1.67262192369e-27, "unit": "kg", "symbol": "m_p"},
    "elementary charge": {"value": 1.602176634e-19, "unit": "C", "symbol": "e"}
}

def get_physics_constant(constant_name: str) -> str:
    """
    Looks up a physical constant from a predefined dictionary.
    Returns the constant's value, unit, and symbol as a JSON string or a descriptive string if not found.
    """
    query_name = constant_name.lower().strip().replace("_", " ") # Normalize input

    if query_name in CONSTANTS:
        return json.dumps(CONSTANTS[query_name])

    # Try partial matching or synonyms
    for key, val_dict in CONSTANTS.items():
        if query_name in key:
            return json.dumps(val_dict)

    return json.dumps({"error": f"Constant '{constant_name}' not found."})

# Example Usage (for testing)
if __name__ == "__main__":
    print(get_physics_constant("speed of light"))
    print(get_physics_constant("gravity"))
    print(get_physics_constant("Boltzmann Constant"))
    print(get_physics_constant("unknown_constant"))