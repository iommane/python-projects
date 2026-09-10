from config import DATABASE_PATH
from database import DataBase
from library import Library
from tabulate import tabulate


class App:
    def __init__(self, lb: Library):
        self.library = lb
        self.running = True

    @staticmethod
    def show_menu() -> None:
        guides = [
            ["/add", "add a new book"],
            ["/books", "view all books"],
            ["/view [id]", "view a specific book"],
            ["/borrow [id]", "borrow a book"],
            ["/return [id]", "return borrowed books"],
            ["/remove [id]", "remove a book"],
            ["/summary", "summary of books"],
            ["/exit", "exit from application"],
        ]

        print(
            tabulate(
                guides,
                headers=["Commands", "Description"],
                tablefmt="rounded_outline",
            )
        )

    def validate_id(self, query) -> int | None:
        try:
            if len(query) < 2:
                raise ValueError("Id required")
            book_id = int(query[1])

            if book_id <= 0:
                raise ValueError("Id must be positive")
            return book_id
        except ValueError:
            print("Invalid id")
            return None

    @staticmethod
    def format_book(book) -> str:
        return (
            f"Book ID: {book.book_id}\n"
            f"Book Name: {book.book_name}\n"
            f"Book Author: {book.author_name}\n"
            f"Available: {'Yes' if book.is_available else 'No'}"
        )

    def handle_commands(self) -> None:
        query = input("> ").strip().split()

        if not query:
            print("Invalid query")
            return

        match query[0].lower():
            case "/add":
                self.add_book()
            case "/books":
                self.show_books()
            case "/view":
                book_id = self.validate_id(query)
                if book_id is None:
                    return
                self.view_book(book_id)
            case "/borrow":
                book_id = self.validate_id(query)
                if book_id is None:
                    return
                self.borrow_book(book_id)
            case "/return":
                book_id = self.validate_id(query)
                if book_id is None:
                    return
                self.return_book(book_id)
            case "/remove":
                book_id = self.validate_id(query)
                if book_id is None:
                    return
                self.remove_book(book_id)
            case "/summary":
                self.book_summary()
            case "/exit":
                self.running = False
            case _:
                print("Invalid query")

    def add_book(self) -> None:
        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()

        if not title or not author:
            print("Invalid title or author")
            return

        if len(title) > 200 or len(author) > 100:
            print("Title or author too long")
            return

        self.library.add_book(title, author)
        print("New book added in the library")

    def show_books(self) -> None:
        books = self.library.show_books()

        if not books:
            print("No book in the library")
            return

        print("\n---- Books ----")
        for book in books:
            print(self.format_book(book), "\n")

    def view_book(self, book_id: int) -> None:
        book = self.library.view_book(book_id)

        if book is None:
            print("Book is not in the library")
            return

        print("\nBook details:")
        print(self.format_book(book) + "\n")

    def borrow_book(self, book_id: int) -> None:
        result = self.library.borrow_book(book_id)

        if result == "not_found":
            print("Book not in the library")
        elif result == "not_available":
            print("Sorry, book is not available in the library")
        elif result == "success":
            print("You borrowed this book, enjoy reading")

    def return_book(self, book_id: int) -> None:
        result = self.library.return_book(book_id)

        if result == "not_found":
            print("Book not in the library")
        elif result == "already_available":
            print("Book already present in library")
        elif result == "success":
            print("You returned this book to the library")

    def remove_book(self, book_id: int) -> None:
        if not self.library.remove_book(book_id):
            print("Book not in the library")
            return

        print("Book removed from the library")

    def book_summary(self) -> None:
        summary = self.library.book_summary()

        summary_text = (
            f"Total books: {summary['total_books']}\n"
            f"Available: {summary['available_books']}\n"
            f"Borrowed: {summary['borrowed_books']}"
        )

        print(summary_text)

    def run(self):
        print("Welcome to the book management system")
        self.show_menu()

        while self.running:
            self.handle_commands()


if __name__ == "__main__":
    database = DataBase(DATABASE_PATH)
    try:
        library = Library(database)
        app = App(library)
        app.run()

    except KeyboardInterrupt:
        print("Stopped")

    finally:
        database.close()
        print("See you later")
