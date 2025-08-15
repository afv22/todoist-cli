"""Todoist API client wrapper."""

from todoist_api_python.api import TodoistAPI
import click


def get_todoist_client(token: str) -> TodoistAPI:
    """Create and return a Todoist API client."""
    try:
        return TodoistAPI(token)
    except Exception as e:
        click.echo(f"Error: Failed to initialize Todoist API client: {e}")
        raise click.Abort()


def list_projects(token: str) -> None:
    """List all active projects with hierarchical structure."""
    try:
        api = get_todoist_client(token)
        projects_iterator = api.get_projects()
        
        # Flatten the iterator of lists into a single list
        all_projects = []
        for project_list in projects_iterator:
            all_projects.extend(project_list)

        if not all_projects:
            click.echo("No projects found.")
            return

        click.echo("Active Projects:")
        click.echo("-" * 40)

        # Create a map of parent projects and their children
        parent_projects = []
        child_projects = {}
        
        for project in all_projects:
            if hasattr(project, 'parent_id') and project.parent_id:
                # This is a subproject
                if project.parent_id not in child_projects:
                    child_projects[project.parent_id] = []
                child_projects[project.parent_id].append(project)
            else:
                # This is a top-level project
                parent_projects.append(project)

        # Display projects hierarchically
        for project in parent_projects:
            # Show parent project
            indicators = []
            if hasattr(project, "is_favorite") and project.is_favorite:
                indicators.append("★")

            indicator_str = f" ({', '.join(indicators)})" if indicators else ""
            click.echo(f"• {project.name}{indicator_str}")
            
            # Show child projects with indentation
            if hasattr(project, 'id') and project.id in child_projects:
                for child in child_projects[project.id]:
                    child_indicators = []
                    if hasattr(child, "is_favorite") and child.is_favorite:
                        child_indicators.append("★")
                    
                    child_indicator_str = f" ({', '.join(child_indicators)})" if child_indicators else ""
                    click.echo(f"  ├─ {child.name}{child_indicator_str}")

    except Exception as e:
        click.echo(f"Error: Failed to fetch projects: {e}")
        raise click.Abort()
