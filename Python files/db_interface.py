import sqlite3
import logging
import traceback
import sys

class DBInterface():
    def __init__(self, name):
        self.name = name

        self.connect()
        self.createTables()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.name)
        except sqlite3.OperationalError as e:
            self.logger.error('Database location incorrectly set, {}'.format(e))
            sys.exit()
        self.c = self.conn.cursor()
        self.c.execute("PRAGMA foreign_keys = ON;")

    def close(self):
        self.c.close()
        self.conn.close()

    '''
    Create tables if they do not exist
    '''
    def createTables(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS bin
            (source_id INTEGER PRIMARY KEY ASC,
            name varchar(10) UNIQUE,
            description var(50));
        """)

        self.c.execute("""CREATE TABLE IF NOT EXISTS distance_value(
            series_id INTEGER PRIMARY KEY ASC,
            timestamp INTEGER,
            distance INTEGER,
            source_id INT,
            FOREIGN KEY (source_id) REFERENCES bin(source_id));
        """)

    """Insert a new bin.
    Args:
        name: Bin name has to be unique.
        description: Description of the bin (optional).
    Raises:
        sqlite3.IntegrityError: If name is not unique
    """
    def insertBin(self, name, description=""):
        try:
            self.c.execute("""INSERT INTO bin (name, description) 
                VALUES (?, ?)""", (name, description))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Bin '{}' already exists".format(name))
            return False
        return self.c.lastrowid

    def getAllBins(self):
        sql = """
            SELECT * FROM bin
        """
        self.c.execute(sql)
        return self.c.fetchall()

    """Select a bin by source_id.
    Args:
        source_id: Source ID.
    Returns:
        Tuple with source_id, name and description of bin if exists.
    """
    def selectBinBySource(self, source_id):
        self.c.execute("""SELECT source_id, name, description FROM bin 
            WHERE source_id=?""", (source_id,))
        ret = self.c.fetchone()
        return ret

    # Insert and select distance values
    def insertDistance(self, timestamp, distance, source_id):
        self.c.execute("""INSERT INTO distance_value
            (timestamp, distance, source_id)
            VALUES (?, ?, ?)""",
            (timestamp, distance, source_id))
        self.conn.commit()

    # TODO: add limit to output
    def selectDistance(self, source_id):
        self.c.execute("""SELECT source_id, timestamp, distance
            FROM distance_value
            WHERE source_id = ?
            ORDER BY timestamp ASC
            LIMIT 100;""", (source_id, ))
        return self.c.fetchall()
