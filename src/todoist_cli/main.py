"""Main CLI entry point for Todoist CLI wrapper."""

import click


@click.group()
@click.version_option()
def cli():
    """Todoist CLI - A command-line interface for Todoist."""
    pass


@cli.command()
def status():
    """Show current status and configuration."""
    click.echo("Todoist CLI v0.1.0")
    click.echo("Status: Ready (SDK connection not implemented yet)")


if __name__ == "__main__":
    cli()