"""
Function to execute a Python file
"""

import subprocess

from google.genai import types

from functions.helpers import get_absolute_path, is_path_inside_working_dir, join_paths, exists_path


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter. If args are not passed, execute the program.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file. If they are not passed, execute the program.",
                ),
                description="Optional arguments to pass to the Python file. If they are not passed, execute the program.",
            )
        },
        required=["file_path"],
    )
)

def run_python_file(working_directory, file_path, args=[]):
    """
    It executes a Python file
    """
    try:
        if not file_path.endswith(".py"):
            raise ValueError(f"\"{file_path}\" is not a Python file.")

        if not is_path_inside_working_dir(working_directory, file_path):
            raise PermissionError(
                f"Cannot execute \"{file_path}\" as it is outside the permitted working directory"
            )

        full_file_path = get_absolute_path(join_paths(working_directory, file_path))
        working_directory_path = get_absolute_path(working_directory)

        if not exists_path(full_file_path):
            raise FileNotFoundError(f"File \"{file_path}\" not found.")

        command_args = ["python3", full_file_path]
        command_args.extend(args)

        completed_process = subprocess.run(
            command_args,
            capture_output=True,
            cwd=working_directory_path,
            check=False,
            timeout=30,
        )

        result = []
        if completed_process.stdout:
            output = completed_process.stdout.decode().strip()
            result.append(f"STDOUT: {output}")

        if completed_process.stderr:
            output = completed_process.stderr.decode().strip()
            result.append(f"STDERR: {output}")

        if completed_process.returncode != 0:
            result.append(f"Process exited with code {completed_process.returncode}")

        return "\n".join(result) if result else "No output produced."

    except Exception as e:
        return f'Error: executing Python file: {e}'
