import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS survey_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        age INTEGER,
                        gender TEXT,
                        genre TEXT
                    )
                """
            )
            conn.commit()

    def execute(self, query: str, params: tuple):
        with sqlite3.connect(self.path) as conn:
            conn.execute(query, params)
            conn.commit()



        
# conn = sqlite3.connect("database.sqlite")
# cursor = conn.cursor()

# conn.execute("""
#     CREATE TABLE IF NOT EXISTS survey_results (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         age INTEGER,
#         gender TEXT,
#         genre TEXT
#     )
# """)

# conn.commit()