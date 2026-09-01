from tabulate import tabulate
from todo import TodoManager


class TodoApp:
    def __init__(self, todo_manager: TodoManager):
        self.todo = todo_manager
        self.running = True

    def show_menu(self) -> None:
        commands = [
            ["/add", "add a new task"],
            ["/view", "view all tasks"],
            ["/complete", "complete a task"],
            ["/delete", "delete a task"],
            ["/help", "get menu"],
            ["/exit", "exit"],
        ]

        print(
            tabulate(
                commands,
                headers=["Commands", "Description"],
                tablefmt="rounded_outline",
            )
        )

    def handle_command(self) -> None:
        query = input("\nWhat you want to do? : ").strip().lower()

        if not query:
            print("Invalid query")
            return

        match query:
            case "/add":
                self.add_task()

            case "/view":
                self.view_tasks()

            case "/delete":
                self.delete_task()

            case "/complete":
                self.complete_task()

            case "/help":
                self.show_menu()

            case "/exit":
                self.running = False
                return

            case _:
                print("Invalid query")
                return

    def add_task(self) -> None:
        name = input("Enter task name: ").strip()

        if not name:
            print("Task name cannot be empty")
            return

        description = input("Enter task description: ").strip()
        task_id = self.todo.add_todo(name, description)
        print(f"New task added -> id : {task_id}")

    def view_tasks(self) -> None:
        tasks = self.todo.view_todo()

        if not tasks:
            print("No task found")
        else:
            print("\n---- All Tasks ----")
            for task_id, task in tasks.items():
                print(f"\nId : {task_id}")
                for key, value in task.items():
                    print(f"{key} : {value}")

            print(f"\nTotal tasks : {len(tasks)}")

    def complete_task(self) -> None:
        task_id = input("Enter task id to complete: ").strip()

        if not task_id:
            print("Id is required")
            return

        if self.todo.complete_todo(task_id):
            print("Status changed to completed")
        else:
            print("No task found with this id")

    def delete_task(self) -> None:
        task_id = input("Enter task id to delete: ").strip()

        if not task_id:
            print("Id is required")
            return

        if self.todo.delete_todo(task_id):
            print("Task deleted")
        else:
            print("No task found with this id")

    def run(self) -> None:
        print("Welcome to Todo CLI")
        self.show_menu()

        while self.running:
            self.handle_command()


if __name__ == "__main__":
    try:
        todo = TodoManager()
        app = TodoApp(todo)
        app.run()

    except KeyboardInterrupt:
        print("\nStopped")

    finally:
        print("See you")
