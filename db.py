#!/usr/bin/env python3
import sqlite3
conn = sqlite3.connect('working.db')


class Database:
    def __init__(self):
        c = conn.cursor()
        # Post table: type is bool indicating request or offer

        #if the count is 1, then table exists
        c.execute('''SELECT count(name) FROM sqlite_master WHERE type="table" and name="Post"''')
        if not c.fetchone()[0]:

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

        c.execute('''INSERT INTO Post VALUES(
                3, 'this is a test', 4, 'South Bend, IN', 'construction', NULL, NULL, NULL, NULL, 1
                )''')

        for row in c.execute('''SELECT * FROM Post'''):
            print(row)

        conn.commit()

if __name__ == '__main__':
    db = Database()
