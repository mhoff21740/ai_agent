import os
from google.generativeai import types

def write_file(working_directory, file_path, content):
    try:
       
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        full_working = os.path.abspath(working_directory)
        if not full_path.startswith(full_working):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


        
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file that is constrained to the working directory.",
    parameters={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to write to, relative to the working directory.",
            },
            "content": {
                "type": "string",
                "description": "The text content to write to the file.",
            },
        },
        "required": ["file_path", "content"]
    }
)

    
    
    
 