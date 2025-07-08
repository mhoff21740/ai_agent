import os

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


        
    
    
    
    
 