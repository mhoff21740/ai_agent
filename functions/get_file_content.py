import os
from functions.config import MAX_CHARS
from google.generativeai import types

def get_file_content(working_directory, file_path):
    try:
        # Resolve full, normalized file path
        combined_full_path = os.path.abspath(os.path.join(working_directory, file_path))
        full_work_path = os.path.abspath(working_directory)

        # Ensure the file stays within the working directory
        if not combined_full_path.startswith(full_work_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure it's a real file
        if not os.path.isfile(combined_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read file safely
        with open(combined_full_path, "r", encoding="utf-8") as f:
            file_content = f.read()

        # Truncate if needed
        if len(file_content) > MAX_CHARS:
            truncated = file_content[:MAX_CHARS]
            return f"{truncated}...File \"{file_path}\" truncated at {MAX_CHARS} characters."

        return file_content
    except Exception as e:
        return f"Error: {e}"



schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads content within a file that is constrained to the working directory.",
    parameters={
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
            }
        },
        "required": [] 
    }
)