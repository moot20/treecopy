# TreeCopy

A command-line tool that generates a tree structure of directories and copies it to the clipboard.

## Features

- Generates tree structure of directories
- Automatically copies output to clipboard
- Respects .gitignore patterns
- Ignores common directories like .git, __pycache__, node_modules
- Clean, readable output format

## Installation

You can install TreeCopy using either uv or pip:

### Using uv (recommended)

```bash
uv pip install git+https://github.com/moot20/treecopy.git
```

### Using pip

```bash
python -m pip install git+https://github.com/moot20/treecopy.git
```

## Usage

```bash
# Generate tree structure and copy to clipboard (default)
treecopy /path/to/directory

# Generate tree structure without copying to clipboard
treecopy /path/to/directory --no-clipboard
```

## Example Output

```
my-project/
├── src/
│   ├── main.py
│   └── utils/
│       └── helpers.py
├── tests/
│   └── test_main.py
├── README.md
└── pyproject.toml
```

## Requirements

- Python 3.12 or higher
- Dependencies are automatically installed:
  - click
  - pyperclip
  - pathspec

## License

This project is licensed under the MIT License - see the LICENSE file for details.