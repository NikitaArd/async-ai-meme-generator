import sqlite3
from db.decorators import handle_db_errors

from config.settings import DATABASE_FILE_NAME

class DBController:
    def __init__(self, db_name=DATABASE_FILE_NAME):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
        self.connect()
        self.create_tables()
        
    @handle_db_errors("Error connecting to database")
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
            
    @handle_db_errors("Error creating table")
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meme_source TEXT NOT NULL,
                meme_description TEXT NOT NULL,
                meme_examples TEXT NOT NULL
            )
        ''')
        self.conn.commit()
            
    @handle_db_errors("Error inserting a record")
    def insert_meme(self, meme_source, meme_description, meme_examples):
        self.cursor.execute('''
            INSERT INTO memes (meme_source, meme_description, meme_examples)
            VALUES (?, ?, ?)
        ''', (meme_source, meme_description, meme_examples))
        self.conn.commit()
            
    @handle_db_errors("Error selecting records")
    def select_memes(self) -> dict[str:tuple]:
        self.cursor.execute('SELECT id, meme_source, meme_description, meme_examples FROM memes')
        
        raw_memes = self.cursor.fetchall()
        
        return {meme[0]: (*meme[1::],) for meme in raw_memes}
    
    @handle_db_errors("Error selecting a row")
    def select_meme(self, *args, **kwargs):
        pass
            
    @handle_db_errors("Error closing a database")
    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")
