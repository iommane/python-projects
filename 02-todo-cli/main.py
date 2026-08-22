def menu():
    message = "\n----- Menu ----\n"
    message += "/add - add task\n"
    message += "/view - check all tasks\n"
    message += "/complete [id] - change task status to complete\n"
    message += "/delete [id] - delete task\n"
    message += "/menu - check commands\n"
    message += "/exit - exit CLI"

    print(message)


def create_task(task_name: str, description: str):
    global generate_id

    generate_id += 1
    task_id = generate_id
    
    tasks[task_id] = {
        "task_name" : task_name,
        "description" : description,
        "status" : "pending"
        }

    print(f"New task added {task_id}")


def check_tasks():
    if not tasks:
        print("No tasks found")
    else:
        total_tasks = len(tasks)
        print("\n---- Tasks ----")
        for task_id, task in tasks.items():
            message = f"Id: {task_id}\n"
            message += f"Name: {task['task_name']}\n"
            message += f"Description: {task['description']}\n"
            message += f"Status: {task['status']}\n"

            print(message)
        print(f"Total tasks : {total_tasks}")


def delete_task(task_id:int):
    if task_id not in tasks:
        print(f"No task with id {task_id} found")
    else:
        tasks.pop(task_id)
        print(f"Task with {task_id} deleted")


def complete_task(task_id: int):
    if task_id not in tasks:
        print(f"No task with id {task_id} found")
    else:
        if tasks[task_id]['status'] != "completed":
            tasks[task_id]['status'] = "completed"
            print("Task status changed")
        else:
            print("Task already completed")


print("Welcome to Todo CLI")
tasks = {}
generate_id = 0
menu()

while True:
    try:
        choice = input("\nEnter your choice: ").strip().lower()
        commands = choice.split()

        if not commands:
            continue

        option = commands[0]

        match option:
            case "/menu":
                menu()
                
            case "/add":
                task_name = input("Enter task name: ").strip()
                if not task_name:
                    print("Task name cannot be empty")
                    continue
                description = input("Enter task description: ").strip()
                create_task(task_name, description)

            case "/view":
                check_tasks()

            case "/complete":
                if len(commands) == 1:
                    task_id = int(input("Enter task id: "))
                elif len(commands) == 2:
                    task_id = int(commands[1])
                else:
                    print("Usage: /complete [id]")
                    continue              

                complete_task(task_id)

            case "/delete":
                if len(commands) == 1:
                    task_id = int(input("Enter task id: "))
                elif len(commands) == 2:
                    task_id = int(commands[1])
                else:
                    print("Usage: /delete [id]")
                    continue

                delete_task(task_id)

            case "/exit":
                print("See you")
                break

            case _:
                print("Invalid choice")

    except ValueError:
        print("Invalid input")

    except KeyboardInterrupt:
        print("Stopped")
        exit()