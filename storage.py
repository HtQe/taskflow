"""Saving and loading tasks as JSON."""
import json

DATA_FILE = "tasks.json"


def load_tasks(path=DATA_FILE):
    """Load tasks from disk. A missing or broken file gives an empty list."""
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    if not isinstance(data, list):
        return []
    return [
        task for task in data
        if isinstance(task, dict) and {"id", "title", "done"} <= task.keys()
    ]


def save_tasks(tasks, path=DATA_FILE):
    """Write tasks to disk as JSON."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2, ensure_ascii=False)
