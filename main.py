import os
import argparse
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types
from functions.get_files_info  import get_files_info, schema_get_files_info 
from functions.get_file_content import  get_file_content ,schema_get_file_content
from functions.write_file import  write_file, schema_write_file
from functions.run_python import run_python_file, schema_run_python 




FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python": run_python_file,
}

# Gemini tool declaration list
AVAILABLE_FUNCTIONS = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python,
    ],
)



SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


# ────────────────────────────────────────────────────────────────────────────────
#  Helper: extract FunctionCall parts from a Gemini response
# ────────────────────────────────────────────────────────────────────────────────

def extract_function_calls(response: genai.types.GenerateContentResponse):
    """Return a list of FunctionCall objects pulled from all candidates."""
    calls = []
    for cand in response.candidates:
        for part in cand.content.parts:
            call = getattr(part, "function_call", None)
            if call is not None:
                calls.append(call)
    return calls



def extract_function_calls(response: genai.types.GenerateContentResponse):
    """Pull any function calls out of the Content parts."""
    calls: list[types.FunctionCall] = []
    for cand in response.candidates:
        for part in cand.content.parts:
            # In the current SDK each `part` has a `.function_call` attr
            call = getattr(part, "function_call", None)
            if call:  # Only append if it's not None
                calls.append(call)
    return calls



#  Main  


def main():
    # Argument parsing ----------------------------------------------------------
    parser = argparse.ArgumentParser(description="CLI wrapper around Gemini that can call local file helpers")
    parser.add_argument("prompt", help="User prompt for Gemini")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Environment / API key -----------------------------------------------------
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not found in .env")
    genai.configure(api_key=api_key)

    # Build model ---------------------------------------------------------------
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-001",
        system_instruction=SYSTEM_PROMPT,
    )

    user_message = {"role": "user", "parts": [args.prompt]}

    # First model call ----------------------------------------------------------
    response = model.generate_content(
        contents=[user_message],
        tools=[AVAILABLE_FUNCTIONS],
    )

    # Verbose token usage -------------------------------------------------------
    if args.verbose:
        um = response.usage_metadata
        print("\n[Verbose]")
        print(f"Prompt tokens : {um.prompt_token_count}")
        print(f"Response tokens : {um.candidates_token_count}\n")

    # Check for function calls --------------------------------------------------
    calls = extract_function_calls(response)
    if calls:
        if calls:
            for call in calls:
                # call.args is a proto map – convert to a normal dict
                call_args = dict(call.args)
                # Inject working_directory if the function expects it
                if "working_directory" not in call_args:
                    call_args["working_directory"] = os.getcwd()
                print(f"Calling function: {call.name}({call_args})")
            fn = FUNCTION_MAP.get(call.name)
            if fn:
                try:
                    result = fn(**call_args)
                except Exception as exc:
                    result = f"Error: {exc}"
            else:
                result = f"Error: No handler implemented for {call.name}"
            print("Function result:" + str(result))
    else:
        print("\nModel response:\n" + response.text)


if __name__ == "__main__":
    main()
