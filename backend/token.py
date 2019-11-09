# Token -> user uuid database

import sqlite3
import os
from time import time
from uuid import uuid1

from constants import DATABASE_FILE

class TokenTable:

    SQL_CREATE_TABLE = '''create TABLE if not exist token (
                            token varchar(100),
                            uuid varchar(100),
                            expire_time int,
                            Primary Key(token)
                        )'''

    TABLE_PATH = os.path.expanduser(DATABASE_PATH)

    SQL_EXISTS = 'SELECT * from Tokens where uuid=? and token=?'
    SQL_INSERT_POST = 'INSERT INTO Tokens (token, uuid, expire_time) VALUES (?, ?, ?)'

    MAX_TTL = 69

    def __init__(self):
        ''' Initialize SQL Table '''
        self.conn = sqlite3.connect(self.TABLE_PATH)

        with self.conn:
            curs = self.conn.cursor()
            curs.execute(self.SQL_CREATE_TABLE)

    def _get_epoch_time(self) -> int:
        ''' returns current epoch time '''
        return int(time())

    def _get_ttl(self) -> int:
        ''' returns time + MAX_TTL constant '''
        return self._get_epoch_time() + self.MAX_TTL

    def validate(self, uid: str, token_id: str) -> bool:
        ''' Checks if userid has token and the token is valid '''
        self.conn = sqlite3.connect(self.TABLE_PATH)

        with self.conn:
            curs = self.conn.cursor()
            # perform query
            curs.execute(self.SQL_EXISTS, (uid, token_id,))
            # check if there is a response
            data = curs.fetchone()
            if not data: return False
            # check if time is expired or nah
            return self._get_epoch_time() < data[2]

    def create(self, uid: str) -> str:
        ''' Create token in table '''
        self.conn = sqlite3.connect(self.TABLE_PATH)

        with self.conn:
            curs = self.conn.cursor()
            # create token
            tok = str(uuid1())
            # insert to table
            curs.execute(self.SQL_INSERT_POST, (tok, uid, self._get_ttl()))

