import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("students.db")


def initialize_database():
    """Reset the lab database and create five fictional/local practice records."""
    connection = sqlite3.connect(DB_PATH)
    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                name TEXT NOT NULL,
                program TEXT NOT NULL,
                year INTEGER NOT NULL,
                section TEXT NOT NULL,
                source TEXT DEFAULT 'Local'
            )
        """)
        # Ensure this script also upgrades an existing Activity 7/8 database.
        columns = {
            row[1] for row in connection.execute("PRAGMA table_info(students)").fetchall()
        }
        if "source" not in columns:
            connection.execute("ALTER TABLE students ADD COLUMN source TEXT DEFAULT 'Local'")

        # This setup script resets the table to the five practice records each time it runs.
        connection.execute("DELETE FROM students")
        connection.execute("DELETE FROM sqlite_sequence WHERE name = 'students'")
        students = [
            ("LAB9-001", "Alex Sample", "BSIT", 1, "A", "Local"),
            ("LAB9-002", "Jamie Example", "BSIT", 2, "B", "Local"),
            ("LAB9-003", "Taylor Demo", "BSCS", 2, "A", "Local"),
            ("LAB9-004", "Morgan Practice", "BSHM", 3, "C", "Local"),
            ("LAB9-005", "Casey Student", "BSED", 1, "D", "Local"),
        ]
        connection.executemany("""
            INSERT INTO students (student_id, name, program, year, section, source)
            VALUES (?, ?, ?, ?, ?, ?)
        """, students)
        connection.commit()
    finally:
        connection.close()
    print("Database created successfully")


if __name__ == "__main__":
    initialize_database()
