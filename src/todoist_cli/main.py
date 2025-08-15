"""Main CLI entry point for Todoist CLI wrapper."""

import click

from .auth import with_token
from .client import list_projects, list_tasks
from .config import get_or_prompt_token, get_stored_token, reset_token


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    """Todoist CLI - A command-line interface for Todoist."""
    # Ensure token is available for commands that need it
    ctx.ensure_object(dict)
    ctx.obj['token'] = None


@cli.command()
@click.pass_context
def status(ctx):
    """Show current status and configuration."""
    click.echo("Todoist CLI v0.1.0")
    
    token = get_stored_token()
    if token:
        click.echo("Status: Token configured ✓")
        click.echo(f"Token: {token[:8]}...{token[-4:] if len(token) > 12 else ''}")
    else:
        click.echo("Status: No token configured")
        click.echo("Run any command to be prompted for your API token.")


@cli.command()
def configure():
    """Configure or reconfigure the Todoist API token."""
    click.echo("Configuring Todoist API token...")
    token = get_or_prompt_token()
    click.echo("Configuration complete!")


@cli.command()
def reset():
    """Reset (remove) the stored API token."""
    if click.confirm("Are you sure you want to remove your stored API token?"):
        reset_token()
    else:
        click.echo("Cancelled.")


@cli.command()
@with_token
def projects(token):
    """List all active projects."""
    list_projects(token)


@cli.command()
@click.option('--project-name', help='Filter tasks by project name')
@with_token
def tasks(token, project_name):
    """List all tasks, optionally filtered by project."""
    list_tasks(token, project_name)


if __name__ == "__main__":
    cli()