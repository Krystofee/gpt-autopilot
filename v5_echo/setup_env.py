#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

from print_color import print_colored_text

def create_virtual_env(project_dir):
    venv_path = os.path.join(project_dir, '.venv')
    if not os.path.exists(venv_path):
        print_colored_text("***** Creating virtual environment *****", f"venv path: {venv_path}", "green")
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
    else:
        print_colored_text("***** Virtual environment already exists *****", f"venv path: {venv_path}", "red")

def get_venv_python(project_dir):
    return os.path.join(project_dir, '.venv', 'bin', 'python')

def install_requirements(project_dir):
    requirements_path = os.path.join(project_dir, 'requirements.txt')
    if os.path.exists(requirements_path):
        print_colored_text("***** Installing requirements *****", f"requirements path: {requirements_path}", "green")
        subprocess.check_call([get_venv_python(project_dir), '-m', 'pip', 'install', '-r', requirements_path])
    else:
        print_colored_text("***** No requirements.txt found *****", f"requirements path: {requirements_path}", "red")

def run_main_script(project_dir):
    main_script_path = os.path.join(project_dir, 'main.py')
    if os.path.exists(main_script_path):
        print_colored_text("***** Running main script *****", f"main script path: {main_script_path}", "green")
        subprocess.check_call([get_venv_python(project_dir), main_script_path])
    else:
        print_colored_text("***** No main.py found *****", f"main script path: {main_script_path}", "red")


def run_project(project_dir):
    create_virtual_env(project_dir)
    install_requirements(project_dir)
    run_main_script(project_dir)


def main():
    parser = argparse.ArgumentParser(description="Set up Python environment, install dependencies, and run main.py.")
    parser.add_argument('project_dir', type=str, help="Directory containing the project")

    args = parser.parse_args()
    project_dir = args.project_dir

    create_virtual_env(project_dir)
    install_requirements(project_dir)
    run_main_script(project_dir)

if __name__ == "__main__":
    main()
