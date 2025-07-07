import os
from dotenv import load_dotenv
import argparse
import google.generativeai as genai


def main():

# --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="A CLI Tool that can contact Google's Gemini LLM")
    parser.add_argument("prompt", help='The prompt to send to Gemini')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

# --- Load Environment Variables ---
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file")
        exit(1)

# --- Configure Gemini Key ---
    genai.configure(api_key=api_key)

 # --- Format the prompt for Gemini Using Updated Google.generativeai docs ---
    messages = [
        {"role": "user", "parts": [args.prompt]}
    ]

# --- Initialize the Model ---
    model = genai.GenerativeModel("gemini-2.0-flash-001")
    response = model.generate_content(contents=messages)




    if args.verbose:
        print("\n[Verbose Output]")
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            
    else:
        print("\nModel response:")
        print(response.text)

if __name__ == "__main__":
    main()