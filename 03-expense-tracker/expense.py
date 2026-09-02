import json


class ExpenseHandler:
    def __init__(self):
        self.expenses = self.load_expenses()
        self.next_id = max(map(int, self.expenses.keys()), default=0) + 1

    def load_expenses(self) -> dict:
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

            print("New record json created")
            return {}

    def save_expenses(self) -> None:
        with open("records.json", "w") as file:
            json.dump(self.expenses, file, indent=4)

    def get_expenses(self) -> dict:
        return self.expenses

    def add_expense(self, amount: float, category: str, date: str) -> str:
        if amount <= 0 or amount > 1_000_000:
            raise ValueError("Amount is not valid")

        if len(category) > 50:
            raise ValueError("Category is too long")

        record_id = str(self.next_id)

        self.expenses[record_id] = {
            "amount": round(amount, 2),
            "category": category,
            "date": date,
        }

        self.save_expenses()
        self.next_id += 1
        return record_id

    def delete_expense(self, record_id: str) -> bool:
        if record_id not in self.expenses:
            return False

        self.expenses.pop(record_id)
        self.save_expenses()
        return True

    def get_summary(self) -> dict:
        if self.expenses:
            total_amount = sum(record["amount"] for record in self.expenses.values())
            highest = max(record["amount"] for record in self.expenses.values())
            lowest = min(record["amount"] for record in self.expenses.values())
            average = total_amount / len(self.expenses)

            summary = {
                "total": round(total_amount, 2),
                "highest": highest,
                "lowest": lowest,
                "average": round(average, 2),
                "count": len(self.expenses),
            }
            return summary

        return {}
