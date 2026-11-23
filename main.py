"""TaskFlow - command-line task manager (menu loop, all input/printing)."""
from manager import TaskManager, TaskNotFoundError
from storage import Storage

MENU = "\n1 Add · 2 List · 3 Complete · 4 Delete · 5 Quit"


def ask_id(prompt):
    """Ask for a task id; return None if the user typed something else."""
    text = input(prompt).strip()
    if not text.isdigit():
        print("Please type a number.")
        return None
    return int(text)


def show_tasks(manager):
    tasks = manager.list()
    if not tasks:
        print("No tasks yet.")
    for task in tasks:
        print(task)


def main():
    manager = TaskManager(Storage())
    while True:
        print(MENU)
        choice = input("> ").strip()
        try:
            if choice == "1":
                task = manager.add(input("Title: "))
                print(f"Added #{task.id}")
            elif choice == "2":
                show_tasks(manager)
            elif choice == "3":
                task_id = ask_id("Task id: ")
                if task_id is not None:
                    manager.complete(task_id)
                    print("Done!")
            elif choice == "4":
                task_id = ask_id("Task id: ")
                if task_id is not None:
                    manager.delete(task_id)
                    print("Deleted.")
            elif choice == "5":
                print("Bye!")
                break
            else:
                print("Choose 1-5.")
        except (ValueError, TaskNotFoundError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
