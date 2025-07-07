



import os
from dotenv import load_dotenv
import google.generativeai as genai




load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")



genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash-001")

response = model.generate_content("Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")

print("Model response:")
print(response.text)



print("\nTokens used:")
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")




def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
