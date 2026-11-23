"""TaskManager: the business logic. No print() or input() here."""
from models import Task


class TaskNotFoundError(Exception):
    """Raised when no task has the requested id."""


class TaskManager:
    """Keeps the task list and saves it through a Storage object."""

    def __init__(self, storage):
        self.storage = storage
        self.tasks = storage.load()

    def find(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"No task with id {task_id}")

    def add(self, title):
        new_id = max((task.id for task in self.tasks), default=0) + 1
        task = Task(new_id, title)
        self.tasks.append(task)
        self.save()
        return task

    def complete(self, task_id):
        task = self.find(task_id)
        task.mark_done()
        self.save()
        return task

    def delete(self, task_id):
        task = self.find(task_id)
        self.tasks.remove(task)
        self.save()
        return task

    def list(self):
        return list(self.tasks)

    def save(self):
        self.storage.save(self.tasks)
