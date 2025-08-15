"""Configuration management for Todoist CLI."""

import os
from pathlib import Path
from typing import Optional

import click


def get_config_dir() -> Path:
    """Get the configuration directory for the CLI."""
    config_dir = Path.home() / ".config" / "todoist-cli"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_token_file() -> Path:
    """Get the path to the token file."""
    return get_config_dir() / "token"


def get_stored_token() -> Optional[str]:
    """Get the stored API token if it exists."""
    token_file = get_token_file()
    if token_file.exists():
        try:
            return token_file.read_text().strip()
        except Exception:
            return None
    return None


def store_token(token: str) -> None:
    """Store the API token securely."""
    token_file = get_token_file()
    token_file.write_text(token)
    # Set restrictive permissions (owner read/write only)
    token_file.chmod(0o600)


def prompt_for_token() -> str:
    """Prompt the user to enter their Todoist API token."""
    click.echo("Welcome to Todoist CLI!")
    click.echo("To get started, you need to provide your Todoist API token.")
    click.echo("You can find your token at: https://todoist.com/prefs/integrations")
    click.echo()
    
    token = click.prompt("Please enter your Todoist API token", hide_input=True)
    
    if not token or not token.strip():
        click.echo("Error: Token cannot be empty.")
        raise click.Abort()
    
    return token.strip()


def get_or_prompt_token() -> str:
    """Get the stored token or prompt for one if it doesn't exist."""
    token = get_stored_token()
    
    if token:
        return token
    
    token = prompt_for_token()
    store_token(token)
    click.echo("Token saved successfully!")
    return token


def reset_token() -> None:
    """Remove the stored token."""
    token_file = get_token_file()
    if token_file.exists():
        token_file.unlink()
        click.echo("Token removed successfully.")