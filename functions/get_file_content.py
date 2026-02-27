from config import MAX_CHARS
import os
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents in a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read contents from, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return print(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

    if not os.path.isfile(target_dir):
        return print(f'Error: File not found or is not a regular file: "{file_path}"')
    
    with open(target_dir, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == 0:
            return print(f'Error: "{file_path}" is empty')

        if len(file_content_string) < len(f.read(MAX_CHARS+1)):
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    return file_content_string
