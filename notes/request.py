import sqlite3
import json
from models import Note

def get_single_note(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            n.id,
            n.concept,
            n.date,
            n.entry,
            n.mood_id
        FROM notes n
        WHERE n.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an note instance from the current row
        note = Note(data['id'], data['concept'], data['date'],
                            data['entry'], data['mood_id'])

        return json.dumps(note.__dict__)

def get_note_by_search_term(search_term):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            n.id,
            n.concept,
            n.date,
            n.entry,
            n.mood_id
            FROM Notes n
            WHERE entry LIKE ?;
        """, ( "%" + search_term + "%", ))

        # Initialize an empty list to hold all note representations
        notes = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an note instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # note class above.
            note = Note(row['id'], row['concept'], row['date'],
                            row['entry'], row['mood_id'])

            notes.append(note.__dict__)

            # Use `json` package to properly serialize list as JSON
        return json.dumps(notes)

def delete_note(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM notes
        WHERE id = ?
        """, (id, ))

def get_all_notes():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            n.id,
            n.concept,
            n.date,
            n.entry,
            n.mood_id
        FROM notes n
        """)

        # Initialize an empty list to hold all note representations
        notes = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an note instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # note class above.
            note = Note(row['id'], row['concept'], row['date'],
                            row['entry'], row['mood_id'])

            notes.append(note.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(notes)