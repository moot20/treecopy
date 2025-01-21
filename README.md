# TreeCopy 🌲
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line tool that generates a tree structure of directories and copies it to the clipboard.

## Features

- Generates tree structure of directories
- Automatically copies output to clipboard
- Easy to use with LLMs like Claude or ChatGPT for context
- Respects .gitignore patterns
- Ignores common directories like .git, \__pycache__, node_modules

**Example Output**

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


## Quick Usage

Run directly without installing:

```bash
uv run https://raw.githubusercontent.com/moot20/treecopy/main/src/treecopy/cli.py /path/to/directory
```

## Installation (optional)

If you prefer to install it as a command:

```bash
# Using uv (recommended)
uv pip install git+https://github.com/moot20/treecopy.git
```

```bash
# Using pip
python -m pip install git+https://github.com/moot20/treecopy.git
```

```bash
# Then use it as a command
treecopy /path/to/directory
```

## Options

```bash
# Don't copy to clipboard
treecopy /path/to/directory --no-clipboard
```

## Requirements

- Python 3.12 or higher
- Dependencies (automatically installed by uv):
  - click
  - pyperclip
  - pathspec

## License

This project is licensed under the MIT License - see the LICENSE file for details.