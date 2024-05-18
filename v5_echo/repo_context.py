import os
import subprocess
import argparse

def get_non_ignored_files(repo_path):
    """Get a list of files not ignored by gitignore in the specified repository."""

    # Get a list of all files tracked by git
    result = subprocess.run(['git', 'ls-files'], stdout=subprocess.PIPE)
    files = result.stdout.decode('utf-8').split('\n')

    return [f for f in files if f]

def read_file_content(filepath):
    """Read the content of a file and return it."""
    with open(filepath, 'r') as file:
        return file.read()

def repository_context(repo_path):
    """Build the formatted output for the repository context and files."""
    os.chdir(repo_path)

    files = get_non_ignored_files(repo_path)
    output = []

    # Repository context
    output.append("$ START_REPOSITORY_CONTEXT $\n")

    output.append("filenames:")
    for file in files:
        if file == '.gitignore':
            continue
        output.append(f"- {file}")

    output.append("")  # Add a newline between sections

    # File contents
    for file in files:
        if file == '.gitignore':
            continue
        content = read_file_content(file)
        output.append(f"FILENAME: {file}\n")
        output.append("CONTENT:\n")
        output.append(content)
        output.append(f"END_CONTENT\n")

    output.append("$ END_REPOSITORY_CONTEXT $\n")

    # Chdir back to the original directory
    os.chdir('..')

    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List files in a git repository that are not ignored by .gitignore and show their contents.')
    parser.add_argument('path', type=str, help='Path to the git repository')

    args = parser.parse_args()
    repo_path = args.path

    if not os.path.isdir(repo_path):
        print(f"The path {repo_path} does not exist or is not a directory.")
        exit(1)

    output = repository_context(repo_path)
    print(output)
