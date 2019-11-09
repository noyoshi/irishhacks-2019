# Token -> user uuid database

import sqlite3
import os
from time import time

from constants import DATABASE_FILE

class TokenTable:

    SQL_CREATE_TABLE = '''create TABLE if not exist token (
                            token varchar(100),
                            uuid varchar(100),
                            expire_time int,
                            Primary Key(token)
                        )'''

    TABLE_PATH = os.path.expanduser(DATABASE_PATH)

    MAX_TTL = 69

    def __init__(self):
        ''' Initialize SQL Table '''
        self.conn = sqlite3.connect(self.TABLE_PATH)

        with self.conn:
            curs = self.conn.cursor()
            curs.execute(self.SQL_CREATE_TABLE)

    def _get_epoch_time(self):
        ''' returns current epoch time '''
        return int(time())

    def validate(self, uid, token_id):
        ''' Checks if userid has token and the token is valid '''
        
        
    def create(self, uid):
        ''' Create token in table '''
