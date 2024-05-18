import os
import platform
import sys

current_directory = os.getcwd()

PROJECT_DIRECTORY = os.path.join(current_directory, "project")

os_version = platform.release()

if len(sys.argv) > 1:
    OBJECTIVE = sys.argv[1]
elif os.path.exists(os.path.join(current_directory, "objective.txt")):
    with open(os.path.join(current_directory, "objective.txt")) as f:
        OBJECTIVE = f.read()

assert OBJECTIVE, "OBJECTIVE missing"
