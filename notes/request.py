from models.note import Note
import models
import sqlite3
import json
from models import Note

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