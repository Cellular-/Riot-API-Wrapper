import sqlite3

class Database():
    def __init__(self, db_path):
        if not db_path:
            raise Exception('You must pass in a path to the database file.')
        
        self.db_path = db_path
        self.conn = None
        self.db_cursor = None
        self.results = None

    def dict_factory(self, cursor, row):
        """Converts database results into a dictionary where the 
        key is the column name and the value is the column value.
        """
        results = {}
        for index, col_name in enumerate(cursor.description):
            results[col_name[0]] = row[index]

        return results

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = self.dict_factory

    def cursor(self):
        self.db_cursor = self.conn.cursor()
    
    def execute(self, query):
        self.connect()
        self.cursor()
        self.db_cursor.execute(query)
        return self

    def get_results(self):
        self.results = self.db_cursor.fetchall()
        self.conn.close()
        return self
    
    def format(self):
        if not self.results:
            raise Exception('There must be database results to format!')

        result = ''
        for record in self.results:
            for key, value in record.items():
                result += f'{key} : {value}\n'

        return result