import json


class TodoManager:
    def __init__(self):
        self.todos = self.load_todo()
        self.next_id = self.generate_id()

    def load_todo(self) -> dict:
        try:
            with open("todo.json", "r") as file:
                todo = json.load(file)

            return todo
        except FileNotFoundError:
            with open("todo.json", "w") as file:
                json.dump({}, file, indent=4)

            return {}

        except json.JSONDecodeError:
            print("Warning: todo.json was invalid, starting with empty")
            with open("todo.json", "w") as file:
                json.dump({}, file, indent=4)

            return {}

    def save_todo(self) -> None:
        with open("todo.json", "w") as file:
            json.dump(self.todos, file, indent=4)

    def generate_id(self) -> int:
        if not self.todos:
            return 1

        return max(map(int, self.todos.keys())) + 1

    def add_todo(self, name: str, description: str) -> str:
        task_id = str(self.next_id)

        self.todos[task_id] = {
            "name": name,
            "description": description,
            "status": "pending",
        }

        self.save_todo()
        self.next_id += 1

        return task_id

    def view_todo(self) -> dict:
        return self.todos

    def delete_todo(self, task_id: str) -> bool:
        if task_id not in self.todos:
            return False

        self.todos.pop(task_id)
        self.save_todo()
        return True

    def complete_todo(self, task_id: str) -> bool:
        if task_id not in self.todos:
            return False

        if self.todos[task_id]["status"] == "completed":
            return True

        self.todos[task_id]["status"] = "completed"
        self.save_todo()
        return True
