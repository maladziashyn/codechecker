"""
Print results of pyflakes {file} to stdout.
Only .py files are checked. See "exclude" for directories and files.
Run optionally with --target to specify target directory
and optionally with --excluded to exclude files from the scan.
"""

import argparse
import subprocess
import sys

from os import getcwd, walk
from os.path import basename, isdir, join


def main():
    parser = argparse.ArgumentParser(description="Filter out excluded files")
    parser.add_argument(
        "-t", "--target",
        type=str,
        # required=True,
        help="Target directory to scan",
    )
    parser.add_argument(
        "-e", "--excluded",
        type=str,
        default="",
        help="Comma-separated list of filenames to exclude"
    )

    args = parser.parse_args()

    # Validate target directory
    if not args.target:
        target_directory = getcwd()
    else:
        if not isdir(args.target):
            print(f"Error: '{args.target}' is not a valid directory",
                file=sys.stderr)
            sys.exit(1)
        else:
            target_directory = args.target
    print(f"Target:\t\033[36m{target_directory}\033[0m")

    # Normalize excluded files
    excluded_files = list()
    if args.excluded:
        excluded_files = [f.strip() for f in args.excluded.split(",")]
        print(f"Excluded files: {excluded_files}")

    file_list = []
    # Excluded directories by default.
    exclude = set([
        "venv", "static_source", "staticfiles", "templates",
        "__pycache__", "migrations"
    ])
    for root, dirs, files in walk(target_directory):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            if file.endswith(".py"):
                file_list.append(join(target_directory, root, file))

    try:
        with open(
            join(target_directory, "_dev", "codechecker_ignored.txt"),
            "r"
        ) as proj_files:
            project_files_ignored = [
                join(target_directory, line.strip())
                for line in proj_files
            ]
    except FileNotFoundError:
        project_files_ignored = list()
    print(f"Ignore:\t{len(project_files_ignored)}")

    check_result = ""
    for file in file_list:
        if (basename(file) not in excluded_files
            and file not in project_files_ignored):
            try:
                process = subprocess.run(
                    ["pyflakes", file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,  # Redirect stderr to stdout
                    text=True,  # Decode output to string
                    check=True  # Raise an exception on non-zero exit code
                )
                result = process.stdout
            except subprocess.CalledProcessError as e:
                result = e.stdout  # Capture the output even in case of error
            if len(result) > 0:
                check_result += result + "\n"

    if len(check_result) > 0:
        print("Result:\t\033[1;31mfail\033[0m\n")
        print(check_result.strip("\n"), "\n")
    else:
        print("Result:\t\033[1mOK\033[0m")


if __name__ == "__main__":
    main()
