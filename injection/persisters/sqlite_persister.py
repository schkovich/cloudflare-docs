import sqlite3
from sqlite3 import Error

class SQLitePersister:
    def __init__(self, db_file):
        """
        Args:
            db_file (str): Path to the SQLite database file.
        """
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def get_cursor(self):
        if self.cursor = None:
            self.cursor = self.conn.cursor()

        return self.cursor

    def connect(self):
        """
        Create a database connection to the SQLite database specified by db_file.
        """
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
            raise  # Raising the exception again

    def disconnect(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def persist_data(self, sql, data):
        cursor = self.get_cursor()
        cursor.execute(sql, content)
        # conn.commit() is not needed. Autocommit is on by default
        return cursor.lastrowid
