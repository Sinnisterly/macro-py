import sqlite3
import json
import os
from appdirs import user_data_dir

class DatabaseManager:
    def __init__(self, app_name='MacroTool', app_author='YourCompanyName'):
        self.app_data_dir = user_data_dir(app_name, app_author)
        if not os.path.exists(self.app_data_dir):
            os.makedirs(self.app_data_dir)
        
        self.db_file = os.path.join(self.app_data_dir, 'macros.db')
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS macros (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                actions TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS hotkeys (
                id INTEGER PRIMARY KEY,
                macro_id INTEGER,
                hotkey TEXT UNIQUE NOT NULL,
                FOREIGN KEY (macro_id) REFERENCES macros (id)
            )
        ''')
        self.conn.commit()

    def save_macro(self, name, actions):
        actions_json = json.dumps(actions)
        self.cursor.execute('INSERT OR REPLACE INTO macros (name, actions) VALUES (?, ?)', (name, actions_json))
        self.conn.commit()

    def get_macro(self, name):
        self.cursor.execute('SELECT actions FROM macros WHERE name = ?', (name,))
        result = self.cursor.fetchone()
        if result:
            return json.loads(result[0])
        return None

    def delete_macro(self, name):
        self.cursor.execute('DELETE FROM macros WHERE name = ?', (name,))
        self.cursor.execute('DELETE FROM hotkeys WHERE macro_id IN (SELECT id FROM macros WHERE name = ?)', (name,))
        self.conn.commit()

    def get_all_macros(self):
        self.cursor.execute('SELECT name, actions FROM macros')
        return {name: json.loads(actions) for name, actions in self.cursor.fetchall()}

    def save_hotkey(self, macro_name, hotkey):
        self.cursor.execute('SELECT id FROM macros WHERE name = ?', (macro_name,))
        macro_id = self.cursor.fetchone()
        if macro_id:
            self.cursor.execute('INSERT OR REPLACE INTO hotkeys (macro_id, hotkey) VALUES (?, ?)', (macro_id[0], hotkey))
            self.conn.commit()

    def get_hotkey(self, macro_name):
        self.cursor.execute('''
            SELECT hotkey FROM hotkeys
            JOIN macros ON hotkeys.macro_id = macros.id
            WHERE macros.name = ?
        ''', (macro_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_all_hotkeys(self):
        self.cursor.execute('''
            SELECT macros.name, hotkeys.hotkey
            FROM hotkeys
            JOIN macros ON hotkeys.macro_id = macros.id
        ''')
        return dict(self.cursor.fetchall())

    def close(self):
        if self.conn:
            self.conn.close()