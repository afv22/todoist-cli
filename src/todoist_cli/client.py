"""Todoist API client wrapper."""

from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Project, Section, Task
from typing import Any, Dict, List, Optional, Iterator
import click


def get_todoist_client(token: str) -> TodoistAPI:
    """Create and return a Todoist API client."""
    try:
        return TodoistAPI(token)
    except Exception as e:
        click.echo(f"Error: Failed to initialize Todoist API client: {e}")
        raise click.Abort()


def _get_projects(token) -> List[Project]:
    api = get_todoist_client(token)
    projects_iterator = api.get_projects()
    return _resolve_iterator(projects_iterator)


def _resolve_iterator(iter: Iterator) -> List[Any]:
    values = []
    for project_list in iter:
        values.extend(project_list)
    return values


def list_projects(token: str) -> None:
    """List all active projects with hierarchical structure."""
    try:
        all_projects = _get_projects(token)

        if not all_projects:
            click.echo("No projects found.")
            return

        click.echo("Active Projects:")
        click.echo("-" * 40)

        # Create a map of parent projects and their children
        parent_projects: List[Project] = []
        child_projects: Dict[str, List[Project]] = {}

        for project in all_projects:
            if project.parent_id:
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
            if project.is_favorite:
                indicators.append("★")

            indicator_str = f" ({', '.join(indicators)})" if indicators else ""
            click.echo(f"• {project.name}{indicator_str}")

            # Show child projects with indentation
            if project.id in child_projects:
                for child in child_projects[project.id]:
                    child_indicators = []
                    if child.is_favorite:
                        child_indicators.append("★")

                    child_indicator_str = (
                        f" ({', '.join(child_indicators)})" if child_indicators else ""
                    )
                    click.echo(f"  ├─ {child.name}{child_indicator_str}")

    except Exception as e:
        click.echo(f"Error: Failed to fetch projects: {e}")
        raise click.Abort()


def list_tasks(token: str, project_name: Optional[str] = None) -> None:
    """List all tasks with hierarchical structure for subtasks."""
    try:
        api = get_todoist_client(token)

        # Get all projects to map project_id to project_name
        all_projects = _get_projects(token)
        project_map = {project.id: project.name for project in all_projects}

        # Get all sections to map section_id to section_name
        sections_iterator = api.get_sections()
        all_sections: List[Section] = _resolve_iterator(sections_iterator)

        section_map = {section.id: section.name for section in all_sections}
        target_project_id = None

        # If project name is specified, find the project ID
        if project_name:
            for project in all_projects:
                if project.name.lower() == project_name.lower():
                    target_project_id = project.id
                    break

            if target_project_id is None:
                click.echo(f"Error: Project '{project_name}' not found.")
                return

        # Get tasks
        tasks_iterator = api.get_tasks(project_id=target_project_id)
        all_tasks: List[Task] = _resolve_iterator(tasks_iterator)

        if not all_tasks:
            if project_name:
                click.echo(f"No tasks found in project '{project_name}'.")
            else:
                click.echo("No tasks found.")
            return

        # Display header
        if project_name:
            click.echo(f"📋 {project_name}")
        else:
            click.echo("📋 All Tasks")
        click.echo("=" * 50)

        # Create a map of parent tasks and their subtasks
        subtasks = {}
        for task in all_tasks:
            if task.parent_id:
                if task.parent_id not in subtasks:
                    subtasks[task.parent_id] = []
                subtasks[task.parent_id].append(task)

        # Group tasks by project and section
        projects_sections = {}

        for task in all_tasks:
            if task.parent_id:
                continue  # Skip subtasks, they'll be handled with their parents

            task_project_id = getattr(task, "project_id")
            task_section_id = getattr(task, "section_id")

            project_name_key = project_map.get(task_project_id, "Unknown Project")
            section_name_key = (
                section_map.get(task_section_id, "No Section")
                if task_section_id
                else "No Section"
            )

            if project_name_key not in projects_sections:
                projects_sections[project_name_key] = {}
            if section_name_key not in projects_sections[project_name_key]:
                projects_sections[project_name_key][section_name_key] = []

            projects_sections[project_name_key][section_name_key].append(task)

        # Display tasks grouped by project and section
        for proj_name, sections in projects_sections.items():
            if not project_name:  # Only show project header when showing all projects
                click.echo(f"\n🏢 {proj_name}")
                click.echo("─" * (len(proj_name) + 4))

            for section_name, tasks in sections.items():
                if section_name != "No Section":
                    click.echo(f"\n📂 {section_name}")
                    click.echo("   " + "─" * (len(section_name) + 2))
                elif (
                    len(sections) > 1 or not project_name
                ):  # Show "No Section" only if there are other sections or showing all projects
                    click.echo(f"\n📂 {section_name}")
                    click.echo("   " + "─" * (len(section_name) + 2))

                for task in tasks:
                    # Show parent task
                    task_info = []
                    if hasattr(task, "priority") and task.priority > 1:
                        task_info.append(f"p{task.priority}")
                    if hasattr(task, "due") and task.due:
                        task_info.append(
                            f"due: {task.due.date if hasattr(task.due, 'date') else task.due}"
                        )

                    task_info_str = f" ({', '.join(task_info)})" if task_info else ""
                    click.echo(f"   • {task.content}{task_info_str}")

                    # Show subtasks with indentation
                    if hasattr(task, "id") and task.id in subtasks:
                        for subtask in subtasks[task.id]:
                            sub_info = []
                            if hasattr(subtask, "priority") and subtask.priority > 1:
                                sub_info.append(f"p{subtask.priority}")
                            if hasattr(subtask, "due") and subtask.due:
                                sub_info.append(
                                    f"due: {subtask.due.date if hasattr(subtask.due, 'date') else subtask.due}"
                                )

                            sub_info_str = (
                                f" ({', '.join(sub_info)})" if sub_info else ""
                            )
                            click.echo(f"     ├─ {subtask.content}{sub_info_str}")

        click.echo()  # Add blank line at the end

    except Exception as e:
        click.echo(f"Error: Failed to fetch tasks: {e}")
        raise click.Abort()
