"""
Function to write a file
"""

import os

from functions.helpers import get_absolute_path, is_path_inside_working_dir, join_paths, exists_path


def write_file(working_directory, file_path, content):
    """
    Write the content in a file. It creates the file if it does not exist
    """
    try:
        if not is_path_inside_working_dir(working_directory, file_path):
            raise PermissionError(
                f"Cannot write to \"{file_path}\" as it is outside the permitted working directory"
            )

        file_abspath = get_absolute_path(join_paths(working_directory, file_path))
        file_dir = os.path.dirname(file_abspath)

        if not exists_path(file_dir):
            os.makedirs(file_dir)

        with open(file_abspath, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Successfully wrote to '{file_path}' ({len(content)} characters written)"

    except Exception as e:
        return f'Error: {e}'
