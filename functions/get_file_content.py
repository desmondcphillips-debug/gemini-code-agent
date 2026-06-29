import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
import config
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory) 
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        results = [f"Content of '{file_path}':"]

        if not valid_target_dir:
            invalid_working_directory_error = f'Error: Cannot view "{file_path}" as it is outside the permitted working directory'
            results.append(invalid_working_directory_error)
            return "\n".join(results)

        if not os.path.isfile(target_dir):
            not_file_error =  f'Error: File not found or is not a regular file: "{file_path}"'
            results.append(not_file_error)
            return "\n".join(results)

        with open(target_dir, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):  
                content += "\n" + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
            return results[0] + "\n" + content

    except Exception as e:
        return (f"An error has occured: {e}")