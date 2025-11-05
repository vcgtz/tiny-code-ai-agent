"""
Function to get the information of files in a specific directory
"""

import os

from functions.helpers import get_absolute_path, is_path_inside_working_dir, is_dir, join_paths


def get_files_info(working_directory, directory="."):
    """
    Get a description of all files in a directory
    """
    try:
        if not is_path_inside_working_dir(working_directory, directory):
            raise PermissionError(
                f"Cannot list \"{directory}\" as it is outside the permitted working directory"
            )

        if not is_dir(join_paths(working_directory, directory)):
            raise NotADirectoryError(f"\"{directory}\" is not a directory")

        directory_path = get_absolute_path(join_paths(working_directory, directory))

        file_list = []
        for element in os.listdir(directory_path):
            element_path = get_absolute_path(join_paths(directory_path, element))
            is_element_dir = os.path.isdir(element_path)
            element_size = os.path.getsize(element_path)

            line = f"- {element}: file_size={element_size}, is_dir={is_element_dir}"
            file_list.append(line)

        return "\n".join(file_list)

    except Exception as e:
        return f'Error: {e}'
