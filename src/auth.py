"""Authentication utilities for Todoist CLI."""

import click

from config import get_or_prompt_token


def require_token() -> str:
    """Get the API token, prompting the user if not configured."""
    try:
        return get_or_prompt_token()
    except click.Abort:
        click.echo("Error: API token is required to use this command.")
        raise


def with_token(f):
    """Decorator to ensure a command has access to the API token."""
    def wrapper(*args, **kwargs):
        token = require_token()
        return f(token, *args, **kwargs)
    
    wrapper.__name__ = f.__name__
    wrapper.__doc__ = f.__doc__
    return wrapper