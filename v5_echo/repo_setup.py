import os
import subprocess
import argparse
import shutil

def setup_repository(repo_path):
    """Setup a new git repository at the specified path."""
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)

    os.chdir(repo_path)

    # Initialize git repository
    subprocess.run(['git', 'init'], check=True)

    # Copy .gitignore.template to .gitignore
    gitignore_template = '../.gitignore.template'
    gitignore = '.gitignore'

    if os.path.exists(gitignore_template):
        shutil.copyfile(gitignore_template, gitignore)
    else:
        print(f"No .gitignore.template found in {repo_path}")
        return

    # Create a simple README.md
    readme_path = 'README.md'
    with open(readme_path, 'w') as readme_file:
        readme_file.write("# Repository Title\n\nThis is a simple README file.\n")

    # Add and commit the files
    subprocess.run(['git', 'add', '.gitignore', 'README.md'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit with .gitignore and README.md'], check=True)
    print("Repository setup complete and initial commit created.")

    # chdir back to the original directory
    os.chdir('..')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Setup a git repository with .gitignore and README.md')
    parser.add_argument('path', type=str, help='Path to setup the git repository')

    args = parser.parse_args()
    repo_path = args.path

    if not os.path.isdir(repo_path):
        try:
            os.makedirs(repo_path)
        except OSError as e:
            print(f"Error creating directory {repo_path}: {e}")
            exit(1)

    setup_repository(repo_path)
