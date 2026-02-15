def run_python_file(working_directory, file_path, args=None):

    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return print(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')

    if not os.path.isfile(target_dir):
        return print(f'Error: "{file_path}" does not exist or is not a regular file')

    if not "target_dir".endswith(.py):
        return print(f'Error: "{file_path}" is not a Python file')
