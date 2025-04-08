import sqlite3 as sql
from pathlib import Path
from typing import Optional
import os

class PuzzleDB:
    def __init__(self, id: str):
        self.path = f'{Path(__file__).parent}/db/{id}.db'

    def open(self, create=True) -> bool:
        '''
        Attempts to open the db file.
        
        If create is set to True, the file will be created if it does not exist. 
        If False is returned, do not attempt to interact with the database with other methods.

        Parameters:
            create (bool, optional): Determines whether or not a new file should be created. Defaults to True.

        Returns:
            bool: Whether or not the file was successfully opened.
        '''
        if not create:
            if not os.path.exists(self.path):
                return False
            return True
        self.db = sql.connect(self.path)
        self.cursor = self.db.cursor()
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS puzzledb (
                state INTEGER PRIMARY KEY,
                remoteness INTEGER
            )
            '''
        )
        return True
    
    def insert(self, table: dict[int, int], overwrite=False):
        '''
        Attempts to insert the key, value pairs in the given dictionary into the database.

        Parameters:
            table (dict): The dictionary of values to insert.
            overwrite (bool, optional): Whether the database entries should be overwritten. Defaults to False.
        '''
        if overwrite:
            mod = 'REPLACE'
        else:
            mod = 'IGNORE'
        self.cursor.executemany(
            f'''
            INSERT OR {mod} INTO puzzledb (state, remoteness)
            VALUES (?, ?)
            ''',
            list(table.items())
        )
    
    def get(self, state: int) -> Optional[int]:
        '''
        Attempts to retrieve the remoteness for the given state from the database.

        Parameters:
            state (int): The (hashed) state of the position.
        
        Return:
            Optional[int]: Either the retrieved remoteness, or None if the key does not exist in the database.
        '''
        self.cursor.execute(
            '''
            SELECT remoteness FROM puzzledb
            WHERE state = ?
            ''',
            (state,)
        )
        row = self.cursor.fetchone()
        if row:
            return row[0]
        return None
        
    
    def close(self):
        '''
        Updates the database with any changes made and closes it.
        '''
        self.db.commit()
        self.db.close()