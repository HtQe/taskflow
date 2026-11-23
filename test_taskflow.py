import os
import tempfile
import unittest

from manager import TaskManager, TaskNotFoundError
from models import Task
from storage import Storage


class TaskFlowTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.mkdtemp()
        self.path = os.path.join(folder, "tasks.json")
        self.manager = TaskManager(Storage(self.path))

    def test_add_gives_incrementing_ids(self):
        first = self.manager.add("One")
        second = self.manager.add("Two")
        self.assertEqual((first.id, second.id), (1, 2))

    def test_empty_title_is_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.add("   ")

    def test_complete_and_delete(self):
        task = self.manager.add("Ship it")
        self.manager.complete(task.id)
        self.assertTrue(self.manager.find(task.id).done)
        self.manager.delete(task.id)
        with self.assertRaises(TaskNotFoundError):
            self.manager.find(task.id)

    def test_unknown_id_raises(self):
        with self.assertRaises(TaskNotFoundError):
            self.manager.complete(99)

    def test_tasks_survive_restart(self):
        self.manager.add("Persist me")
        again = TaskManager(Storage(self.path))
        self.assertEqual([t.title for t in again.list()], ["Persist me"])

    def test_broken_file_gives_empty_list(self):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write("{not json")
        self.assertEqual(Storage(self.path).load(), [])

    def test_str_shows_check_mark(self):
        task = Task(1, "Write tests")
        task.mark_done()
        self.assertEqual(str(task), "[✓] 1. Write tests")


if __name__ == "__main__":
    unittest.main()
