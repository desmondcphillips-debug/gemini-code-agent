from google.genai import types
from collections.abc import Callable
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists contents of a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to list content from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specific python file along with its associated arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to a specific python file, relative to the working directory (default is the working directory itself)",
            ),
             "args": types.Schema(
                type=types.Type.STRING,
                description="Arguments to pass through provided python file",
            )
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text to a new file, overwriting current text if file already exists",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to a specific text file, relative to the working directory (default is the working directory itself)",
            ),
             "content": types.Schema(
                type=types.Type.STRING,
                description="Provided text to write to the passed file",
            )
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
)

def call_function(
    function_call: types.FunctionCall, verbose: bool = False
) -> types.Content:
    
    function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
    }
    if "verbose" in function_call.args.values():
        print(f"Calling function: {function_call.name}({function_call.args})")
    print(f" - Calling function: {function_call.name}")

    function_name = function_call.name or ""
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}

    args["working_directory"] = "./calculator"

    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )