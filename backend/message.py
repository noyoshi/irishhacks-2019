import sqlite3
import os
from uuid import uuid1

from constants import DATABASE_FILE

class Message:
    '''
    Class for messages
    '''

    DEFAULT_PATH = os.path.expanduser(DATABASE_FILE) 

    SQL_SELECT_MESSAGE = 'SELECT * FROM Message WHERE mid = ?'
    SQL_INSERT_MESSAGE = 'INSERT INTO Message VALUES(?, ?, ?, ?, ?)'
    SQL_DELETE_MESSAGE = 'DELETE FROM Message WHERE mid = ?'
    SQL_SELECT_READ    = 'SELECT * FROM Message WHERE receiver = ? and read = 1'
    SQL_SELECT_UNREAD  = 'SELECT * FROM Message WHERE receiver = ? and read = 0'
    SQL_SELECT_SENT    = 'SELECT * FROM Message WHERE sender = ?'

    SQL_CREATE_MESSAGE_TABLE = '''CREATE TABLE IF NOT EXISTS Message(
            mid VARCHAR(100) PRIMARY KEY,
            sender VARCHAR(100),
            receiver VARCHAR(100),
            body VARCHAR(255),
            read bool
        )'''

    def __init__(self, sender: str, receiver: str, body: str, mid: str = "", read: bool = False):
        self.mid      = str(uuid1()) if not mid else mid
        self.sender   = sender
        self.receiver = receiver
        self.body     = body
        self.read     = read 

    @classmethod
    def init_table(cls) -> None:
        ''' Attempts to make SQL table if not already existing '''
        conn = sqlite3.connect(Message.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Message.SQL_CREATE_MESSAGE_TABLE)

    @classmethod
    def get_from_mid(cls, mid: str):
        ''' returns message object from mid '''
        conn = sqlite3.connect(Message.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            # call select 
            curs.execute(Message.SQL_SELECT_MESSAGE, (mid, ))
            return curs.fetchone()

    @classmethod
    def get_all_unread(cls, receiver: str):
        ''' returns list of message id's of unread messages '''
        conn = sqlite3.connect(Message.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            # call select
            curs.execute(Message.SQL_SELECT_UNREAD, (receiver, ))
            return [x[0] for x in curs.fetchall() if x]

    @classmethod
    def get_all_read(cls, receiver: str):
        ''' returns list of message id's of read messages '''
        conn = sqlite3.connect(Message.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            # call select
            curs.execute(Message.SQL_SELECT_READ, (receiver, ))
            return [x[0] for x in curs.fetchall() if x]

    @classmethod
    def get_all_sent(cls, sender: str):
        ''' returns list of message id's of sent messages '''
        conn = sqlite3.connect(Message.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            # call select
            curs.execute(Message.SQL_SELECT_SENT, (sender, ))
            return [x[0] for x in curs.fetchall() if x]

    def insert_into_db(self) -> None:
        ''' Insert message into database '''
        conn = sqlite3.connect(DATABASE_FILE)
        with conn:
            curs = conn.cursor()
            ins_tuple = (self.mid, self.sender, self.receiver, self.body, self.read)
            curs.execute(Message.SQL_INSERT_MESSAGE, ins_tuple)
    
    def get_mid(self) -> str:
        return self.mid

    def get_sender(self) -> str:
        return self.sender
    
    def set_sender(self, sender: str) -> None:
        self.sender = sender
    
    def get_receiver(self) -> str:
        return self.receiver
    
    def set_receiver(self, receiver: str) -> None:
        self.receiver = receiver
    
    def get_body(self) -> str:
        return self.body
    
    def set_body(self, body: str) -> None:
        self.body = body

    def get_read(self) -> bool:
        return self.read
    
    def set_read(self, read: bool) -> None:
        self.read = read

if __name__ == '__main__':
    # init table
    Message.init_table()

    # add some messages
    test = Message('bob', 'bill', 'hello there')
    test.insert_into_db()

    conn = sqlite3.connect(DATABASE_FILE)
    with conn: 
        curs = conn.cursor()
        for row in curs.execute('SELECT * from Message'):
            print(row)