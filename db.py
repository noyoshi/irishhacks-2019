#!/usr/bin/env python3
import sqlite3


class Database:
    SQL_CREATE_POST_TABLE = '''CREATE TABLE IF NOT EXISTS Post(
                post_id int NOT NULL PRIMARY KEY,
                description TEXT,
                num_vols INT,
                location VARCHAR(255),
                tag1 VARCHAR(50),
                tag2 VARCHAR(50),
                tag3 VARCHAR(50),
                tag4 VARCHAR(50),
                tag5 VARCHAR(50),
                type BOOL
            )'''

    SQL_CREATE_PERSON_TABLE = '''CREATE TABLE IF NOT EXISTS Person(
                uuid PRIMARY KEY,
                email VARCHAR(100),
                phone CHAR(10),
                name VARCHAR(100),
                bio TEXT,
                dob DATE,

            )'''


    def __init__(self):
        conn = sqlite3.connect('working.db')
        c = conn.cursor()

        # Post table: type is bool indicating request or offer
        c.execute()

        for row in c.execute('''SELECT * FROM Post'''):
            print(row)

        conn.commit()
        conn.close()

if __name__ == '__main__':
    db = Database()
