# codechecker

Custom Python code checker. On top of pyflakes.

## Usage

### Installation

Pip install into a project.

```
pip install /path/to/codechecker/root/directory
```

Optionally in editable mode with `-e`

```
pip install -e /path/to/codechecker/root/directory
```

### Run

Run from project directory from venv:

```
(venv) user@host:~/where/you/are$ codechecker
```

Run with arguments:

```
(venv) user@host:~/where/you/are$ codechecker --target=/target/directory --exclude="list.py,of_files.py,to_exclude.py"
```

`--target` or `-t` is the target root directory.

`--exclude` or `-e` is a comma separated list of files to exclude from the scan.

### Ignored project files

Files listed in `/target/directory/_dev/codechecker_ignored.txt` will be ignored.

Add a full file path per one line.
