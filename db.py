#!/usr/bin/env python3
import sqlite3


class Database:
    def __init__(self):
        conn = sqlite3.connect('working.db')
        c = conn.cursor()

        #if the count is 1, then table exists
        c.execute('''SELECT count(name) FROM sqlite_master WHERE type="table" and name="Post"''')
        if not c.fetchone()[0]:
            # Post table: type is bool indicating request or offer
            c.execute('''CREATE TABLE Post(
                    post_id int NOT NULL PRIMARY KEY,
                    description text,
                    num_vols int,
                    location VARCHAR(255),
                    tag1 VARCHAR(50),
                    tag2 VARCHAR(50),
                    tag3 VARCHAR(50),
                    tag4 VARCHAR(50),
                    tag5 VARCHAR(50),
                    type bool
                )''')

        for row in c.execute('''SELECT * FROM Post'''):
            print(row)

        conn.commit()
        conn.close()

if __name__ == '__main__':
    db = Database()
