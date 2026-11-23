"""Task operations on a list of task dicts.

Each task is a dict: {"id": int, "title": str, "done": bool}.
This module never prints or asks for input; main.py does that.
"""

MAX_TITLE_LENGTH = 100


class TaskNotFoundError(Exception):
    """Raised when no task has the requested id."""


def find_task(tasks, task_id):
    """Return the task with this id or raise TaskNotFoundError."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise TaskNotFoundError(f"No task with id {task_id}")


def add_task(tasks, title):
    """Create a task, append it to the list and return it."""
    title = title.strip()
    if not title:
        raise ValueError("Title cannot be empty")
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(f"Title is longer than {MAX_TITLE_LENGTH} characters")
    new_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": new_id, "title": title, "done": False}
    tasks.append(task)
    return task


def complete_task(tasks, task_id):
    """Mark a task as done and return it."""
    task = find_task(tasks, task_id)
    task["done"] = True
    return task


def delete_task(tasks, task_id):
    """Remove a task from the list and return it."""
    task = find_task(tasks, task_id)
    tasks.remove(task)
    return task


def list_tasks(tasks):
    """Return a copy of the task list."""
    return list(tasks)
