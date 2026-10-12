# run_sql.py
# Runs the SQL in a .sql file against the Brightside database and prints the results as a table.
#
# How to use it (from inside your brightside folder):
#     python run_sql.py lesson04/first_query.sql
#
# You don't need to understand this code yet. Lesson 28 ("Python talks to databases")
# goes through it line by line.

import sqlite3
import sys
import os

folder = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(folder, "brightside.db")


def show_value(value):
    """Turn one value into text for printing. Missing values show as NULL."""
    if value is None:
        return "NULL"
    return str(value)


def print_table(column_names, rows):
    """Print rows as a neat table with a header and a row count."""
    widths = [len(name) for name in column_names]
    for row in rows:
        for position, value in enumerate(row):
            widths[position] = max(widths[position], len(show_value(value)))

    header = " | ".join(name.ljust(widths[i]) for i, name in enumerate(column_names))
    print(header)
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(" | ".join(show_value(value).ljust(widths[i]) for i, value in enumerate(row)))

    if len(rows) == 1:
        print("(1 row)")
    else:
        print("(" + str(len(rows)) + " rows)")
    print()


def run_statement(connection, statement):
    """Run one SQL statement. Print the results if it returns any, or say what changed."""
    try:
        cursor = connection.execute(statement)
    except sqlite3.Error as error:
        print("ERROR:", error)
        print("In this statement:")
        print(statement.strip())
        print()
        return False

    if cursor.description is not None:
        column_names = [column[0] for column in cursor.description]
        print_table(column_names, cursor.fetchall())
    elif cursor.rowcount >= 0:
        print("OK:", cursor.rowcount, "row(s) changed")
        print()
    return True


def main():
    if len(sys.argv) < 2:
        print("Tell me which file to run, e.g.:  python run_sql.py lesson04/first_query.sql")
        return

    sql_file = sys.argv[1]
    if not os.path.exists(database_path):
        print("Can't find brightside.db. Run  python setup_brightside.py  first.")
        return
    if not os.path.exists(sql_file):
        print("Can't find the file", sql_file, "- check the name and the folder you're in.")
        return

    with open(sql_file, encoding="utf-8") as file:
        sql_text = file.read()

    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")

    # Run the file one statement at a time, so every SELECT gets its own table of results
    statement = ""
    for line in sql_text.splitlines(keepends=True):
        statement = statement + line
        if sqlite3.complete_statement(statement):
            run_statement(connection, statement)
            statement = ""

    # A last statement without a semicolon at the end still gets run
    leftover = "\n".join(
        line for line in statement.splitlines() if not line.strip().startswith("--")
    )
    if leftover.strip():
        run_statement(connection, statement)

    connection.commit()
    connection.close()


main()
