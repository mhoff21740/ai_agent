import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Validate input
if len(sys.argv) != 2:
    print('Usage: python3 main.py "your prompt here"')
    sys.exit(1)

# Get the user prompt
user_prompt = sys.argv[1]

# Format messages using a simple dictionary structure
messages = [
    {"role": "user", "parts": [user_prompt]}
]

# Initialize the model
model = genai.GenerativeModel("gemini-2.0-flash-001")

# Generate content using the messages
response = model.generate_content(contents=messages)

# Display output
def main():
    print("\nModel response:")
    print(response.text)
    print("\nTokens used:")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
