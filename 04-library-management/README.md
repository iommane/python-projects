# 📚 Library Management

A simple command-line library management system built with Python and SQLite.

---

## 📂 Project Structure

```text
04-library-management/
├── main.py
├── library.py
├── database.py
├── book.py
├── config.py
├── database.db #automatically created
├── requirements.txt
└── README.md
```

---

## ⭐ Features

- Add new books
- View all books or a specific book
- Borrow and return books
- Remove books from the library
- View a summary of available and borrowed books

--- 

## 🚀 How to run?

1. Create a virtual environment

```bash
python -m venv venv
```

2. Activate the virtual environment

Windows
```bash
venv\Scripts\activate
```

macOS/Linux
```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run:

```bash
python main.py
```

--- 

## 🛠️ Commands

| Command | Description |
|---------|-------------|
| `/add` | Add a new book |
| `/books` | View all books |
| `/view [id]` | View a specific book |
| `/borrow [id]` | Borrow a book |
| `/return [id]` | Return a borrowed book |
| `/remove [id]` | Remove a book |
| `/summary` | View summary of books |
| `/exit` | Exit the application |

---

## 🎯 Goal

This project is part of my Python learning journey, progressing from basic procedural code toward Object-Oriented Programming. I hope this becomes a part of yours as well.