import os
import sys
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    
    try:
        working_dir_abs = os.path.abspath(working_directory) 
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
        
        results = [f"Running python file '{file_path}':"]

        if not valid_target_dir:
            invalid_working_directory_error = f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            results.append(invalid_working_directory_error)
            return "\n".join(results)

        if not os.path.isfile(file_path_abs):
            not_file_error =  f'Error: "{file_path}" does not exist or is not a regular file'
            results.append(not_file_error)
            return "\n".join(results)
        
        if file_path[-3:] != ".py":
            not_python_file_error = f'Error: "{file_path}" is not a Python file'
            results.append(not_python_file_error)
            return "\n".join(results)
        
        command = ["python", file_path_abs]
        if args:
            command.extend(args)
        
        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            exit_code_msg = f"Process exited with code {result.returncode}"
            results.append(exit_code_msg)

        if result.stdout == None and result.stderr == None:
            no_output_msg = f"No output produced"
            results.append(no_output_msg)

        if result.stdout:
            std_out_msg = f"STDOUT: {result.stdout}"
            results.append(std_out_msg)

        if result.stderr:
            std_err_msg = f"STDERR: {result.stderr}"
            results.append(std_err_msg)

        return "\n".join(results)

        
    except Exception as e:
        return (f"An error has occured: {e}")