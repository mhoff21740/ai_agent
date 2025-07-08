import os
import subprocess
from google.generativeai import types


def run_python_file(working_directory, file_path):
        try:
        
            if os.path.isabs(file_path):
                file_path = os.path.relpath(file_path, start=working_directory)
            full_path = os.path.abspath(os.path.join(working_directory, file_path))
            full_working = os.path.abspath(working_directory)
            if not full_path.startswith(full_working):
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            if not os.path.exists(full_path):
                return f'Error: File \"{file_path}\" not found.' 
            name, ext = os.path.splitext(full_path)
            ext = ext.lower()
            if ext != ".py":
                return f'Error: "{full_path}" is not a Python file.'
            capture = subprocess.run(["python3",full_path], text=True, capture_output = True, timeout = 30, cwd=full_working)
            output = []
            if capture.stdout:
                output.append(f"STDOUT:{capture.stdout}")
            if capture.stderr:
                output.append(f"STDERR:{capture.stderr}")
            if capture.returncode != 0:
                output.append(f"Process exited with code {capture.returncode}")
            if not output:
                return "No output produced"
            
            return "\n".join(output)
        except Exception as e:
            return f"Error: executing Python file: {e}"
            
        
schema_run_python = types.FunctionDeclaration(
    name="run_python",
    description="Runs python files that are constrained to the working directory.",
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
        
                    