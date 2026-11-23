# TaskFlow

A command-line task manager built during the Full-Stack bootcamp.
Tasks are saved to `tasks.json`, so they are still there after a restart.

## Features

- Add, list, complete and delete tasks
- Input is validated: typing letters or a wrong id never crashes the app
- Priority for every task: `high`, `medium` (default) or `low`
- The list is sorted by priority and can be filtered: `all`, `open` or `done`

## Project structure

| File | Job |
|------|-----|
| `models.py` | `Task` class (data + behaviour) |
| `manager.py` | `TaskManager`: add, find, complete, delete, list |
| `storage.py` | `Storage`: load and save JSON, safe if the file is missing or broken |
| `main.py` | The menu loop: all input and printing |
| `test_taskflow.py` | Unit tests |

## Run it

```bash
python main.py
```

Menu: `1 Add · 2 List · 3 Complete · 4 Delete · 5 Quit`

## Run the tests

```bash
python -m unittest -v
```

## Git workflow

- Nobody pushes straight to `main`: work on a branch and open a pull request.
- Small commits with clear messages.
