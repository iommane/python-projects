class Book:
    def __init__(
        self, book_id: int, book_name: str, author_name: str, is_available: bool
    ):

        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.is_available = is_available
