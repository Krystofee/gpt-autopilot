import os
import shutil


def repo_remove(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        # print(f"Directory '{directory}' and all its contents have been removed.")
    else:
        pass
