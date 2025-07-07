import os

def get_files_info(working_directory, directory=None):
    combined_path = os.path.join(working_directory, directory)
    combined_path = os.path.abspath(combined_path)
    full_working_path = os.path.abspath(working_directory)
    if not combined_path.startswith(full_working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(combined_path):
        return f'Error: "{directory}" is not a directory'
    info_list = []
    try:
        for item in os.listdir(combined_path):
            full_path = os.path.join(combined_path, item)
            filename = os.path.basename(full_path)
            file_size = os.path.getsize(full_path)
            if os.path.isdir(full_path):
                result = True 
            else:
                result = False
            file_info = f"- {filename}: file_size={file_size} bytes, is_dir={result}\n"
            info_list.append(file_info)
        return "\n".join(info_list)
    except Exception as e:
        return f"Error: {e}"

  
                    
       
    
        



    
    











