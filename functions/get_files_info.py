import os
from google import genai
from google.genai import types


def get_files_info(working_directory: str, directory: str = ".") -> str:
    
    try:
        working_dir_abs = os.path.abspath(working_directory) 
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    except:
        return "Error: Ax exception has occured"
    
    results = [f"Result for '{directory}' directory:"]

    if valid_target_dir == False:
        invalid_working_directory_error = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        results.append(invalid_working_directory_error)
        return "\n".join(results)

    if os.path.isdir(target_dir) == False:
        not_directory_error =  f'Error: "{directory}" is not a directory'
        results.append(not_directory_error)
        return "\n".join(results)
    
    dir_list = os.listdir(target_dir)
    for item in dir_list:
        item_location = "/".join([target_dir, item])
        item_file_size = os.path.getsize(item_location)
        is_directory = os.path.isdir(item_location)
        file_details = f"  - {item}: file_size={item_file_size} bytes, is_dir={is_directory}"
        results.append(file_details)
        
    return "\n".join(results)
    
    