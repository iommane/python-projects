from book import Book


class Library:
    def __init__(self, database):
        self.db = database

    def add_book(self, title: str, author: str):
        self.db.insert_book(title, author)

    def view_book(self, book_id: int) -> Book | None:
        row = self.db.get_book(book_id)

        if row is None:
            return None

        return Book(
            book_id=row[0],
            book_name=row[1],
            author_name=row[2],
            is_available=bool(row[3]),
        )

    def show_books(self) -> list[Book]:
        rows = self.db.get_books()

        books = []
        for book in rows:
            books.append(
                Book(
                    book_id=book[0],
                    book_name=book[1],
                    author_name=book[2],
                    is_available=bool(book[3]),
                )
            )

        return books

    def remove_book(self, book_id: int) -> bool:
        book = self.view_book(book_id)

        if book is None:
            return False

        if not book.is_available:
            return False

        return self.db.delete_book(book_id)

    def borrow_book(self, book_id: int) -> str:
        book = self.view_book(book_id)

        if book is None:
            return "not_found"

        if not book.is_available:
            return "not_available"

        success = self.db.borrow_book(book_id)

        if success:
            return "success"
        else:
            return "not_found"

    def return_book(self, book_id: int) -> str:
        book = self.view_book(book_id)

        if book is None:
            return "not_found"

        if book.is_available:
            return "already_available"

        success = self.db.return_book(book_id)

        if success:
            return "success"
        else:
            return "not_found"

    def book_summary(self) -> dict:
        books = self.show_books()

        total_books = len(books)
        available_books = sum(book.is_available for book in books)
        borrowed_books = total_books - available_books

        return {
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": borrowed_books,
        }
