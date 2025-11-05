"""
Helpers for general purpose
"""

import os


def get_absolute_path(path):
    """
    Return the absolute path
    """
    return os.path.abspath(path)

def is_path_inside_working_dir(working_directory, path):
    """
    Check if a given path is inside of the working directory
    """
    workdir_abspath = get_absolute_path(working_directory)
    abspath = get_absolute_path(os.path.join(working_directory, path))

    return abspath.startswith(workdir_abspath)

def join_paths(base_path, relative_path):
    """
    Return a join between two paths
    """
    return os.path.join(base_path, relative_path)

def is_dir(path):
    """
    Check if a given path is a directory
    """
    return os.path.isdir(path)


def is_file(path):
    """
    Check if a given path is a file
    """
    return os.path.isfile(path)

def exists_path(path):
    """
    Check if a dir or file exists
    """
    return os.path.exists(path)
