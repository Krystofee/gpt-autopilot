#!/usr/bin/env python3

import argparse
import os

from make_refactor_tasks import make_refactor_tasks
from make_tasks import make_tasks
from print_color import print_colored_text
from repo_context import repository_context
from repo_remove import repo_remove
from repo_setup import setup_repository
from setup_env import run_project
from write_code import write_code

def process_files(repository, objective_filename):
    print_colored_text(
        "***** START *****",
        f"repository:     {repository}\n"
        f"objective_filename: {objective_filename}",
        "green"
    )

    with open(objective_filename, 'r') as file:
        objective = file.read()

    setup_repository(repository)

    initial_task_set = make_tasks(objective_filename)
    process_coding_tasks(repository, objective, initial_task_set)

    print_colored_text("***** Now refactoring phase begins! *****", "", "red")

    refactor_task_set = make_refactor_tasks(repository, objective)
    while refactor_task_set:
        print_colored_text("***** Refactor phase *****", "", "red")
        process_coding_tasks(repository, objective, refactor_task_set)
        refactor_task_set = make_refactor_tasks(repository, objective)

    # Run the project
    run_project(repository)


def process_coding_tasks(repository, objective, tasks):
    if not tasks:
        return False

    for task in tasks:
        filename = task['filename']
        description = task['description']

        print_colored_text(
            "***** Task *****",
            f"filename: {filename}\n"
            f"description: {description}",
            "yellow"
        )

        write_code(
            repository=repository,
            filename=filename,
            prompt=description,
            objective=objective,
        )

    return True


def main():
    parser = argparse.ArgumentParser(description="CLI tool to process files.")
    parser.add_argument('repository', type=str, help="Working directory")
    parser.add_argument('prompt', type=str, help="Prompt filename")

    args = parser.parse_args()

    repository = args.repository
    objective_filename = args.prompt

    # Change to the specified working directory
    repo_remove(repository)
    process_files(repository, objective_filename)

if __name__ == "__main__":
    main()
