"""The Task class: data and behaviour together."""

MAX_TITLE_LENGTH = 100


class Task:
    """One task with an id, a title and a done flag."""

    def __init__(self, task_id, title, done=False):
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty")
        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError(
                f"Title is longer than {MAX_TITLE_LENGTH} characters"
            )
        self.id = task_id
        self.title = title
        self.done = done

    def mark_done(self):
        self.done = True

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["title"], data["done"])

    def __str__(self):
        mark = "✓" if self.done else " "
        return f"[{mark}] {self.id}. {self.title}"
