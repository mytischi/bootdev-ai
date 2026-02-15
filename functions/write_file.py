import os

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return print(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')

    if not os.path.isdir(file_path):
        return print(f'Error: Cannot write to "{file_path}" as it is a directory')
    
    # Make sure that all parent directories of the file_path exist.
    os.makedirs(file_path ,exist_ok=True)

    if len(content) == 0:
        return print(f"Error: The input content is empty")

    with open(target_dir, "w") as f:
        f.write(content)
        return print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')




