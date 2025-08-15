# Todoist CLI

A command-line interface wrapper around the Todoist Python SDK.

## Setup

This project uses `uv` for fast Python package management and virtual environments.

### Prerequisites

- Python 3.11+ 
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Create and activate virtual environment:**
   ```bash
   uv venv
   source .venv/bin/activate
   ```

2. **Install the CLI in development mode:**
   ```bash
   uv pip install -e .
   ```

3. **Test the installation:**
   ```bash
   todo --help
   todo status
   ```

### Development

To work on the project:

1. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **Install development dependencies (optional):**
   ```bash
   uv pip install -e ".[dev]"
   ```

### Project Structure

```
todoist-cli/
├── pyproject.toml          # Project configuration and dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
└── src/todoist_cli/
    ├── __init__.py        # Package initialization
    └── main.py            # CLI entry point
```

### Available Commands

- `todo --help` - Show help information
- `todo status` - Show current status and configuration

## License

MIT