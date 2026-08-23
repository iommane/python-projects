import json


class TodoManager:
    def __init__(self):
        self.tasks = self.load_tasks()
        self.next_task_id = self.generate_next_id()

    def load_tasks(self) -> dict:
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)

            return tasks

        except FileNotFoundError:
            with open("tasks.json", "w") as file:
                json.dump({}, file, indent=4)

            return {}

        except json.JSONDecodeError:
            print("Warning: tasks.json was invalid, starting with empty tasks")

            with open("tasks.json", "w") as file:
                json.dump({}, file, indent=4)

            return {}

    def save_tasks(self) -> None:
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file, indent=4)

    def generate_next_id(self) -> int:
        if not self.tasks:
            return 1

        return max(map(int, self.tasks.keys())) + 1

    def get_tasks(self) -> dict:
        return self.tasks

    def create_task(self, task_name: str, description: str) -> str:
        task_id = str(self.next_task_id)

        self.tasks[task_id] = {
            "task_name": task_name,
            "description": description,
            "status": "pending",
        }

        self.save_tasks()
        self.next_task_id += 1

        return task_id

    def delete_task(self, task_id: str) -> bool:
        if task_id not in self.tasks:
            return False

        self.tasks.pop(task_id)
        self.save_tasks()

        return True

    def complete_task(self, task_id: str) -> tuple[bool, str]:
        if task_id not in self.tasks:
            return False, "not found"

        if self.tasks[task_id]["status"] == "completed":
            return True, "is already completed"

        self.tasks[task_id]["status"] = "completed"
        self.save_tasks()

        return True, "status changed to completed"


class TodoApp:
    def __init__(self, todo_manager: TodoManager):
        self.todo = todo_manager
        self.running = True

    def run(self):
        print("Welcome to Todo CLI")
        self.print_menu()

        while self.running:
            try:
                self.handle_command()

            except ValueError:
                print("Invalid input")

            except KeyboardInterrupt:
                print("Stopped")
                self.running = False

    def handle_command(self):
        choice = input("\nEnter your choice: ").strip()
        commands = choice.split()

        if not commands:
            return

        command = commands[0].lower()

        match command:
            case "/add":
                self.add_task()

            case "/view":
                self.view_tasks()

            case "/delete":
                self.delete_task(commands)

            case "/complete":
                self.complete_task(commands)

            case "/menu":
                self.print_menu()

            case "/exit":
                self.running = False

            case _:
                print("Choose from options")
                return

    def print_menu(self):
        message = "\n----- Menu ----\n"
        message += "/add - add task\n"
        message += "/view - check all tasks\n"
        message += "/complete [id] - change task status to complete\n"
        message += "/delete [id] - delete task\n"
        message += "/menu - check commands\n"
        message += "/exit - exit CLI"

        print(message)

    def add_task(self):
        name = input("Enter task name: ").strip()

        if not name:
            print("Task name cannot be empty")
            return

        description = input("Enter task description: ").strip()
        task_id = self.todo.create_task(name, description)

        print(f"New task added id : {task_id}")

    def view_tasks(self):
        tasks = self.todo.get_tasks()

        if not tasks:
            print("No task found")
        else:
            print("\n---- Tasks ----")
            for task_id, task in tasks.items():
                message = f"Id: {task_id}\n"
                message += f"Name: {task['task_name']}\n"
                message += f"Description: {task['description']}\n"
                message += f"Status: {task['status']}\n"

                print(message)

            print(f"Total tasks : {len(tasks)}")

    def complete_task(self, commands: list):
        if len(commands) == 1:
            task_id = input("Enter task id: ").strip()
        elif len(commands) == 2:
            task_id = commands[1]
        else:
            print("Usage: /complete [id]")
            return

        is_complete, message = self.todo.complete_task(task_id)

        if is_complete:
            print(f"Task id {task_id} {message}")
        else:
            print(f"Error: task id {task_id} {message}")

    def delete_task(self, commands: list):
        if len(commands) == 1:
            task_id = input("Enter task id: ").strip()
        elif len(commands) == 2:
            task_id = commands[1]
        else:
            print("Usage: /delete [id]")
            return

        is_deleted = self.todo.delete_task(task_id)

        if is_deleted:
            print(f"Task with id {task_id} deleted")
        else:
            print("No task found with this id")


def main():
    todo = TodoManager()
    app = TodoApp(todo)
    app.run()


if __name__ == "__main__":
    main()
