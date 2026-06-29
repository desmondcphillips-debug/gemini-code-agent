import sys
import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory) 
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        results = [f"Writing to '{file_path}':"]

        if not valid_target_dir:
            invalid_working_directory_error = f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            results.append(invalid_working_directory_error)
            return "\n".join(results)

        if os.path.isdir(target_dir):
            not_file_error =  f'Error: Cannot write to "{file_path}" as it is a directory'
            results.append(not_file_error)
            return "\n".join(results)
        
        parent_dir = os.path.dirname(target_dir)

        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        
        with open(target_dir, "w") as f:
            f.write(content)

        write_success_message =  f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        results.append(write_success_message)
        return "\n".join(results)
    
    except Exception as e:
        return (f"Error: {e}")