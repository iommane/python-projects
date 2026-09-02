from datetime import datetime

from expense import ExpenseHandler
from tabulate import tabulate


class ExpenseApp:
    def __init__(self, expense_handler: ExpenseHandler):
        self.expense = expense_handler
        self.running = True

    def handle_command(self) -> None:
        query = input("\nEnter your choice: ").strip().lower()

        if not query:
            print("Invalid choice")
            return

        match query:
            case "/add":
                self.add_record()

            case "/view":
                self.view_records()

            case "/summary":
                self.show_summary()

            case "/delete":
                self.delete_record()

            case "/help":
                self.show_menu()

            case "/exit":
                self.running = False

            case _:
                print("Invalid command")

    def show_menu(self) -> None:
        commands = [
            ["/add", "add a new transaction"],
            ["/view", "view all transactions"],
            ["/delete", "delete a transaction"],
            ["/summary", "short summary"],
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

    def view_records(self) -> None:
        records = self.expense.get_expenses()

        if not records:
            print("No transaction found")
            return

        print("\n---- Transactions ----")
        for record_id, record in records.items():
            print(f"\nId: {record_id}")
            for key, value in record.items():
                print(f"{key} : {value}")

        print(f"\nTotal transactions: {len(records)}")

    def add_record(self) -> None:
        amt = input("Enter amount: ").strip()
        if not amt:
            print("Amount is required")
            return

        try:
            amount = float(amt)
        except ValueError:
            print("Invalid amount")
            return

        category = input("Enter category: ").strip()
        if not category:
            print("Category is required")
            return

        date = input("Enter date (YYYY-MM-DD): ").strip()
        if not date:
            print("Date is required")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format")
            return

        try:
            record_id = self.expense.add_expense(amount, category, date)
            print(f"Expense added -> Id: {record_id}")
        except ValueError as error:
            print(error)

    def delete_record(self) -> None:
        record_id = input("Enter id to delete: ").strip()

        if not record_id:
            print("Id required")
            return

        is_deleted = self.expense.delete_expense(record_id)

        if is_deleted:
            print("Record is deleted")
        else:
            print("Record not found")

    def show_summary(self) -> None:
        summary = self.expense.get_summary()

        if not summary:
            print("No transactions found")
            return

        print("\n---- Summary ----")
        for key, value in summary.items():
            print(f"{key} : {value}")

    def run(self) -> None:
        print("Welcome to Expense Manager")
        self.show_menu()

        while self.running:
            self.handle_command()


if __name__ == "__main__":
    try:
        expense_handler = ExpenseHandler()
        app = ExpenseApp(expense_handler)
        app.run()

    except KeyboardInterrupt:
        print("\nStopped")

    finally:
        print("See you again")
