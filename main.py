"""TaskFlow v1 - command-line task manager (menu loop, all input/printing)."""
from storage import load_tasks, save_tasks
from tasks import (
    TaskNotFoundError, add_task, complete_task, delete_task, list_tasks,
)

MENU = "\n1 Add · 2 List · 3 Complete · 4 Delete · 5 Quit"


def ask_id(prompt):
    """Ask for a task id; return None if the user typed something else."""
    text = input(prompt).strip()
    if not text.isdigit():
        print("Please type a number.")
        return None
    return int(text)


def show_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
    for task in list_tasks(tasks):
        mark = "✓" if task["done"] else " "
        print(f"[{mark}] {task['id']}. {task['title']}")


def main():
    tasks = load_tasks()
    while True:
        print(MENU)
        choice = input("> ").strip()
        try:
            if choice == "1":
                task = add_task(tasks, input("Title: "))
                print(f"Added #{task['id']}")
            elif choice == "2":
                show_tasks(tasks)
            elif choice == "3":
                task_id = ask_id("Task id: ")
                if task_id is not None:
                    complete_task(tasks, task_id)
                    print("Done!")
            elif choice == "4":
                task_id = ask_id("Task id: ")
                if task_id is not None:
                    delete_task(tasks, task_id)
                    print("Deleted.")
            elif choice == "5":
                save_tasks(tasks)
                print("Saved. Bye!")
                break
            else:
                print("Choose 1-5.")
        except (ValueError, TaskNotFoundError) as error:
            print(f"Error: {error}")
        save_tasks(tasks)


if __name__ == "__main__":
    main()
