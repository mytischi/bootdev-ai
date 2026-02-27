import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content in a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="String of content to write",
                ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_dir):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    # Make sure that all parent directories of the file_path exist.
    os.makedirs(os.path.dirname(target_dir), exist_ok=True)
    
    if len(content) == 0:
        return f"Error: The input content is empty"

    with open(target_dir, "w") as f:
        f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'




