import sqlite3 as sql
from pathlib import Path
import os

class PuzzleDB:
    def __init__(self, id: str):
        path = f'{Path(__file__).parent}/db/{id}.db'
        self.db = sql.connect(path)
        self.cursor = self.db.cursor()
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS puzzledb (
                state INTEGER PRIMARY KEY,
                remoteness INTEGER
            )
            '''
        )
    
    def insert(self, table: dict[int, int], overwrite=False):
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
    
    def get(self, state: int):
        self.cursor.execute(
            f'''
            SELECT remoteness FROM puzzledb
            WHERE state = ?
            ''',
            (state,)
        )
    
    def close(self):
        self.db.commit()
        self.db.close()