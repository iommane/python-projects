import json
from datetime import datetime


class ExpenseHandler:
    def __init__(self):
        self.expenses = self.load_records()
        self.next_id = max(map(int, self.expenses.keys()), default=0) + 1

    def load_records(self) -> dict:
        try:
            with open("records.json", "r") as file:
                records = json.load(file)

            return records

        except FileNotFoundError:
            with open("records.json", "w") as file:
                json.dump({}, file, indent=4)

            print("New record json created")

            return {}

        except json.JSONDecodeError:
            with open("records.json", "w") as file:
                json.dump({}, file, indent=4)

            print("New record json created, old one was corrupted")

            return {}

    def save_records(self) -> None:
        with open("records.json", "w") as file:
            json.dump(self.expenses, file, indent=4)

    def get_records(self) -> dict:
        return self.expenses

    def add_record(self, amount: float, category: str, date: str) -> int:
        # Validate amount
        if amount <= 0:
            raise ValueError("Amount must be positive")

        if amount > 1_000_000:
            raise ValueError("Amount is too large")

        # Validate category
        if not category or not isinstance(category, str):
            raise ValueError("Category required")

        if len(category) > 50:
            raise ValueError("Category too long")

        # Validate basic date format
        if not date or len(date) < 8:
            raise ValueError("Invalid date format")

        record_id = str(self.next_id)

        self.expenses[record_id] = {
            "amount": round(amount, 2),
            "category": category.strip(),
            "date": date,
        }

        self.save_records()
        self.next_id += 1
        return record_id

    def delete_record(self, record_id: str) -> bool:
        if record_id not in self.expenses:
            return False

        self.expenses.pop(record_id)
        self.save_records()

        return True

    def get_summary(self) -> tuple[float, float, int]:
        if len(self.expenses) > 0:
            total_amount = 0

            for record in self.expenses.values():
                total_amount += record.get("amount")

            average = total_amount / len(self.expenses)

            return round(total_amount, 2), round(average, 2), len(self.expenses)

        return 0, 0, 0


class ExpenseApp:
    def __init__(self, expense_handler: ExpenseHandler):
        self.expense = expense_handler
        self.running = True

    def run(self):
        self.print_menu()

        while self.running:
            try:
                self.handle_command()

            except ValueError:
                print("Invalid input")

            except KeyboardInterrupt:
                print("Stopped")
                self.running = False

            except EOFError:
                print("Input ended")
                self.running = False

    def handle_command(self):
        option = input("\nEnter your choice: ")

        if not option:
            print("Invalid choice")
            return

        match option:
            case "/add":
                self.add_record()

            case "/view":
                self.check_record()

            case "/summary":
                self.check_summary()

            case "/delete":
                self.delete_record()

            case "/menu":
                self.print_menu()

            case "/exit":
                self.running = False

            case _:
                print("Invalid command")

    def print_menu(self):
        message = "\n---- Menu ----\n"
        message += "/add - add transaction\n"
        message += "/view - view all records\n"
        message += "/delete - delete a record\n"
        message += "/summary - short summary\n"
        message += "/menu - get menu options\n"
        message += "/exit - exit"

        print(message)

    def check_record(self):
        records = self.expense.get_records()

        if not records:
            print("No records found")
            return

        print("\n---- Transactions ----\n")
        for record_id, record in records.items():
            message = f"Id: {record_id}\n"
            message += f"Amount: {record.get('amount')}\n"
            message += f"Category: {record.get('category')}\n"
            message += f"Date: {record.get('date')}\n"

            print(message)
        print(f"Total transactions: {len(records)}")

    def add_record(self):
        amt = input("Enter amount: ").strip()

        if not amt:
            print("Amount required")
            return

        try:
            amount = float(amt)
        except ValueError:
            print("Invalid amount")
            return

        category = input("Enter category: ").strip()

        if not category:
            print("Category required")
            return

        date = input("Enter date (YYYY-MM-DD): ").strip()
        if not date:
            print("Date required")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")  # noqa: DTZ007

        except ValueError:
            print("Invalid date format")
            return

        record_id = self.expense.add_record(amount, category, date)

        print(f"Expense added -> Id: {record_id}")

    def delete_record(self):
        record_id = input("Enter id to delete: ").strip()

        if not record_id:
            print("Id required")
            return

        is_deleted = self.expense.delete_record(record_id)

        if is_deleted:
            print(f"Record {record_id} is deleted")
        else:
            print(f"Not found record with this id : {record_id}")

    def check_summary(self):
        total, average, count = self.expense.get_summary()

        if total != 0:
            print(
                f"\n---- Expense Summary ----\nTotal: ₹{total}\nAverage: ₹{average}\nCount: {count}"
            )

        else:
            print("No transactions found")


def main():
    expense_handler = ExpenseHandler()
    app = ExpenseApp(expense_handler)
    app.run()


if __name__ == "__main__":
    main()
