import sqlite3


class DataBase:
    def __init__(self, db_path: str):
        try:
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
            self.db_path = db_path
            self.create_table_books()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError(
                f"Failed to connect to database at {db_path}: {e}"
            ) from e

    def create_table_books(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_name TEXT NOT NULL,
                author_name TEXT NOT NULL,
                is_available BOOLEAN DEFAULT TRUE)
                """)
            self.connection.commit()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError(f"Failed to create table : {e}") from e

    def insert_book(self, title: str, author: str):
        try:
            self.cursor.execute(
                """
                INSERT INTO books (book_name, author_name) 
                VALUES (?, ?)""",
                (title, author),
            )
            self.connection.commit()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError(f"Failed to insert book : {e}") from e

    def delete_book(self, b_id: int) -> bool:
        try:
            self.cursor.execute(
                """DELETE FROM books WHERE book_id = ?
            """,
                (b_id,),
            )
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError(f"Failed to delete book : {e}") from e

    def get_book(self, b_id: int):
        try:
            self.cursor.execute(
                """
                SELECT * FROM books
                WHERE book_id = ?
                """,
                (b_id,),
            )
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError(f"Failed to get book {b_id}: {e}") from e

    def get_books(self) -> list[tuple]:
        try:
            self.cursor.execute("""
                SELECT * FROM books
                """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError(f"Failed to get books : {e}") from e

    def borrow_book(self, b_id: int) -> bool:
        try:
            self.cursor.execute(
                """
                UPDATE books SET is_available = FALSE WHERE book_id = ?
                """,
                (b_id,),
            )
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError(f"Failed to borrow book : {e}") from e

    def return_book(self, b_id: int) -> bool:
        try:
            self.cursor.execute(
                """
                UPDATE books SET is_available = TRUE WHERE book_id = ?
                """,
                (b_id,),
            )
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError(f"Failed to return book : {e}") from e

    def close(self):
        try:
            if self.connection:
                self.connection.close()
        except sqlite3.Error as e:
            raise sqlite3.DatabaseError(f"Failed to close : {e}") from e
