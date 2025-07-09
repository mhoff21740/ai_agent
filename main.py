import os
import argparse
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types
from functions.get_files_info  import get_files_info, schema_get_files_info 
from functions.get_file_content import  get_file_content ,schema_get_file_content
from functions.write_file import  write_file, schema_write_file
from functions.run_python import run_python_file, schema_run_python 
from typing import Any



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

def call_function(function_call_part, verbose= False) -> dict:
    
    function_name = function_call_part.name
    function_args = dict(function_call_part.args or {})
    function_args["working_directory"] = "./calculator"   

    if function_name != "get_files_info" and "directory" in function_args:
        function_args["file_path"] = function_args.pop("directory")

    if verbose:
        print(f"Calling function: {function_name}({function_args})")


    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    fn = FUNCTION_MAP.get(function_name)
    if fn is None:
        # unknown function
        payload = {"error": f"Unknown function: {function_name}"}
    else:
        # run it, catching exceptions
        try:
            payload = {"result": fn(**function_args)}
        except Exception as exc:
            payload = {"error": f"{exc}"}

    # return a plain-dict “tool” message
    return {
        "role": "tool",
        "parts": [
            {
                "function_response": {
                    "name": function_name,
                    "response": payload,
                }
            }
        ],
    }


        
            
    






def extract_function_calls(resp: genai.types.GenerateContentResponse):
    calls = []
    for cand in resp.candidates or []:
        for part in cand.content.parts:
            call = getattr(part, "function_call", None)
            if call:
                calls.append(call)
    return calls


# ───────────────────────────────────────────────────────────────────────────────
def call_function(call: Any, verbose=False) -> dict:
    fn_name  = call.name
    fn_args  = dict(call.args or {})
    fn_args["working_directory"] = "./calculator"

    # normalise “directory” → “file_path” for file-based functions
    if fn_name != "get_files_info" and "directory" in fn_args:
        fn_args["file_path"] = fn_args.pop("directory")

    if verbose:
        print(f"Calling function: {fn_name}({fn_args})")
    else:
        print(f" - Calling function: {fn_name}")

    fn = FUNCTION_MAP.get(fn_name)
    if not fn:
        payload = {"error": f"Unknown function: {fn_name}"}
    else:
        try:
            payload = {"result": fn(**fn_args)}
        except Exception as exc:
            payload = {"error": str(exc)}

    # package as a “tool” message
    return {
        "role": "tool",
        "parts": [
            {
                "function_response": {
                    "name": fn_name,
                    "response": payload,
                }
            }
        ],
    }


def main():
    
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", help="Initial user prompt")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY") or ""
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY missing")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-001",
        system_instruction=SYSTEM_PROMPT,
    )

    # running conversation
    messages = [{"role": "user", "parts": [args.prompt]}]

    for step in range(20):       
        try:
            resp = model.generate_content(
                contents=messages,
                tools=[AVAILABLE_FUNCTIONS],
            )
        except Exception as exc:
            print(f"Fatal API error: {exc}")
            return

        # append model’s content to history
        for cand in resp.candidates or []:
            messages.append({"role": "model",
                             "parts": cand.content.parts})

        # if LLM produced plain text, we’re done
        plain_text = None
        try:
            # Part-wise scan avoids ValueError when a function_call is present
            first_parts = resp.candidates[0].content.parts
            # collect any part that has a .text attribute
            text_chunks = [p.text for p in first_parts if getattr(p, "text", None)]
            plain_text = " ".join(text_chunks).strip() if text_chunks else None
        except Exception:
            plain_text = None
# --------------------------------------------------------------------

        if plain_text:
            print("\nModel response:\n" + plain_text)
            return

        # otherwise look for function calls
        calls = extract_function_calls(resp)
        if not calls:
            print("No function call and no text – stopping.")
            return

        for call in calls:
            tool_msg = call_function(call, verbose=args.verbose)
            # validate structure
            try:
                _ = tool_msg["parts"][0]["function_response"]["response"]
            except Exception:
                raise RuntimeError("Invalid tool response structure")
            # add tool result to chat
            messages.append(tool_msg)
            if args.verbose:
                print(f"-> {_}")

    print("Reached 20 iterations without a final answer.")

if __name__ == "__main__":
    main()