# multi_agent_tutor/config.py
import os
# from dotenv import load_dotenv # Temporarily comment out or remove for this specific test on Railway

# load_dotenv() # Ensure this is commented out or removed for this test

print("---- RAILWAY DEBUG: STARTING CONFIG ----")
gemini_key_from_env = os.getenv("GEMINI_API_KEY")
print(f"RAILWAY DEBUG: Value of GEMINI_API_KEY from os.getenv(): '{gemini_key_from_env}'") # This is the crucial line

print("RAILWAY DEBUG: Listing relevant environment variables from os.environ:")
found_in_os_environ = False
for key, value in os.environ.items():
    if "GEMINI_API_KEY" in key.upper(): # Check for the key itself or similar names
        print(f"RAILWAY DEBUG: Found in os.environ: {key} = '{value[:5]}...' (value partially masked for logs)") # Mask most of it
        found_in_os_environ = True
    elif "RAILWAY_" in key.upper(): # Print Railway-specific variables, they might give clues
        print(f"RAILWAY DEBUG: Found Railway var: {key} = {value}")

if not found_in_os_environ:
    print("RAILWAY DEBUG: GEMINI_API_KEY was NOT explicitly found by iterating os.environ.")


GEMINI_API_KEY = gemini_key_from_env # This is what your app will use

if not GEMINI_API_KEY:
    print("RAILWAY DEBUG: GEMINI_API_KEY is None after os.getenv(). Raising ValueError.")
    raise ValueError("GEMINI_API_KEY not found in Railway environment variables. Please double-check Railway service settings and ensure a full redeploy was done after setting the variable.")
else:
    print(f"RAILWAY DEBUG: GEMINI_API_KEY successfully obtained from Railway environment: '{GEMINI_API_KEY[:5]}...' (partially masked)")

DEFAULT_GEMINI_MODEL = "gemini-1.5-flash-latest"
print("---- RAILWAY DEBUG: CONFIG LOADED ----")