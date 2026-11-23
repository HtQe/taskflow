"""The Task class: data and behaviour together."""

MAX_TITLE_LENGTH = 100
PRIORITIES = ("high", "medium", "low")
DEFAULT_PRIORITY = "medium"


class Task:
    """One task with an id, a title and a done flag."""

    def __init__(self, task_id, title, done=False, priority=DEFAULT_PRIORITY):
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty")
        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError(
                f"Title is longer than {MAX_TITLE_LENGTH} characters"
            )
        priority = priority.strip().lower()
        if priority not in PRIORITIES:
            raise ValueError(
                "Priority must be one of: " + ", ".join(PRIORITIES)
            )
        self.id = task_id
        self.title = title
        self.done = done
        self.priority = priority

    def mark_done(self):
        self.done = True

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["title"],
            data["done"],
            data.get("priority", DEFAULT_PRIORITY),  # old files have none
        )

    def __str__(self):
        mark = "✓" if self.done else " "
        return f"[{mark}] {self.id}. {self.title} ({self.priority})"
