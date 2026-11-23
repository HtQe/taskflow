"""Storage: saving and loading tasks as JSON."""
import json

from models import Task

DATA_FILE = "tasks.json"


class Storage:
    """Reads and writes a list of Task objects to a JSON file."""

    def __init__(self, path=DATA_FILE):
        self.path = path

    def load(self):
        """Return the saved tasks. A missing or broken file gives []."""
        try:
            with open(self.path, encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        tasks = []
        for item in data:
            try:
                tasks.append(Task.from_dict(item))
            except (KeyError, TypeError, ValueError, AttributeError):
                continue  # skip damaged entries instead of crashing
        return tasks

    def save(self, tasks):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(
                [task.to_dict() for task in tasks],
                file, indent=2, ensure_ascii=False,
            )
