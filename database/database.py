import sqlite3

class PuzzleDB:
    def __init__(self, id: str):
        self.db = sqlite3.connect(f'./db/{id}.db')
        self.cursor = self.db.cursor()
        self.cursor.execute(
            '''
            CREATE TABLE [IF NOT EXISTS] puzzledb(
                state INTEGER PRIMARY KEY,
                remoteness INTEGER
            )
            '''
        )
    
    def insert(self, table: dict[int, int]):
        self.cursor.executemany(
            '''
            INSERT INTO puzzledb (state, remoteness)
            VALUES (?, ?)
            ''',
            list(table.items())
        )
    
    def close(self):
        self.db.commit()
        self.db.close()