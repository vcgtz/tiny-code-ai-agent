import os
import subprocess
from config import MAX_CHARS


def get_abspath(path):
    return os.path.abspath(path)

def is_path_inside_working_dir(working_directory, path):
    workdir_abspath = get_abspath(working_directory)
    abspath = get_abspath(os.path.join(working_directory, path))

    return abspath.startswith(workdir_abspath)

def is_path_a_dir(working_directory, path):
    abspath = get_abspath(os.path.join(working_directory, path))

    return os.path.isdir(abspath)

def is_path_a_file(working_directory, path):
    abspath = get_abspath(os.path.join(working_directory, path))

    return os.path.isfile(abspath)

def get_files_info(working_directory, directory="."):
    try:
        if not is_path_inside_working_dir(working_directory, directory):
            raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory')

        if not is_path_a_dir(working_directory, directory):
            raise Exception(f'"{directory}" is not a directory')

        directory_abspath = get_abspath(os.path.join(working_directory, directory))

        file_list = []
        for element in os.listdir(directory_abspath):
            element_path = os.path.abspath(os.path.join(directory_abspath, element))

            is_dir = os.path.isdir(element_path)
            size = os.path.getsize(element_path)

            line = f"- {element}: file_size={size}, is_dir={is_dir}"
            file_list.append(line)

        return "\n".join(file_list)
    except Exception as e:
        return f'Error: {e}'

def get_file_content(working_directory, file_path):
    try:
        if not is_path_inside_working_dir(working_directory, file_path):
            raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')

        if not is_path_a_file(working_directory, file_path):
            raise Exception(f'File not found or is not a regular file: "{file_path}"')

        file_abspath = get_abspath(os.path.join(working_directory, file_path))

        file_content_string = ""
        with open(file_abspath, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        if len(file_content_string) == MAX_CHARS:
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'

        return file_content_string
    except Exception as e:
        return f'Error: {e}'

def write_file(working_directory, file_path, content):
    try:
        if not is_path_inside_working_dir(working_directory, file_path):
            raise Exception(f'Cannot write to "{file_path}" as it is outside the permitted working directory')

        file_abspath = get_abspath(os.path.join(working_directory, file_path))
        file_dir = os.path.dirname(file_abspath)

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        with open(file_abspath, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

def run_python_file(working_directory, file_path, args=[]):
    try:
        if not file_path.endswith(".py"):
            raise Exception(f'"{file_path}" is not a Python file.')

        if not is_path_inside_working_dir(working_directory, file_path):
            raise Exception(f'Cannot execute "{file_path}" as it is outside the permitted working directory')

        file_abspath = get_abspath(os.path.join(working_directory, file_path))
        working_abspath = get_abspath(working_directory)

        if not os.path.exists(file_abspath):
            raise Exception(f'File "{file_path}" not found.')

        completed_process = subprocess.run(
            ["python", file_abspath] + args,
            capture_output=True,
            cwd=working_abspath,
            check=False,
            timeout=30,
        )

        result = ""
        if completed_process.returncode == 0:
            output = completed_process.stdout.decode().strip()
            result += f"STDOUT: {output if output else "No output produced."}\n"
        else:
            output = completed_process.stderr.decode().strip()
            result += f"STDERR: {output if output else "No output produced."}\n"
            result += f"Process exited with code {completed_process.returncode}"

        return result
    except Exception as e:
        return f'Error: executing Python file: {e}'
