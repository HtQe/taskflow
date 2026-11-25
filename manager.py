"""TaskManager: the business logic. No print() or input() here."""
from models import PRIORITIES, Task


class TaskNotFoundError(Exception):
    """Raised when no task has the requested id."""


def count_open(tasks):
    """How many tasks are not done."""
    return sum(not task.done for task in tasks)


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

    def add(self, title, priority="medium"):
        new_id = max((task.id for task in self.tasks), default=0) + 1
        task = Task(new_id, title, priority=priority)
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

    def list(self, status="all"):
        """Return tasks sorted by priority. status: all, open or done."""
        if status not in ("all", "open", "done"):
            raise ValueError("Filter must be all, open or done")
        tasks = [
            task for task in self.tasks
            if status == "all"
            or (status == "done") == task.done
        ]
        return sorted(
            tasks, key=lambda task: (PRIORITIES.index(task.priority), task.id)
        )

    def save(self):
        self.storage.save(self.tasks)
