import os

from config import current_directory


def list_files_recursively(directory):
    files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            files.append(
                os.path.relpath(os.path.join(dirpath, filename), current_directory)
            )
    return files
