import os

def get_files_info(working_directory, directory=None):
    full_path = os.path.join(working_directory, directory)
    full_path = os.path.abspath(full_path)
    if not full_path.startswith(working_directory):
        f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory):
        f'Error: "{directory}" is not a directory'