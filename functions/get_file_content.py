"""
Function to get the content of a specific file
"""

from google.genai import types

from functions.helpers import get_absolute_path, is_path_inside_working_dir, is_file, join_paths
from config import MAX_CHARS


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read the content from, relative to the working directory. It must be provided.",
            )
        },
        required=["file_path"],
    )
)

def get_file_content(working_directory, file_path):
    """
    Get the content of a file or truncate it to 10,000 characters
    """
    try:
        if not is_path_inside_working_dir(working_directory, file_path):
            raise PermissionError(
                f"Cannot read \"{file_path}\" as it is outside the permitted working directory"
            )

        if not is_file(join_paths(working_directory, file_path)):
            raise FileNotFoundError(f"File not found or is not a regular file: \"{file_path}\"")

        full_file_path = get_absolute_path(join_paths(working_directory, file_path))

        file_content_string = ""
        with open(full_file_path, "r", encoding="utf-8") as f:
            file_content_string = f.read(MAX_CHARS)

        if len(file_content_string) == MAX_CHARS:
            file_content_string += f"[...File \"{file_path}\" truncated at 10000 characters]"

        return file_content_string

    except Exception as e:
        return f'Error: {e}'
