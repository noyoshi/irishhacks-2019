# Post.py

import os

import sqlite3

from uuid import uuid1
from typing import List

from constants import DATABASE_FILE


class Post:
    '''
    Class to represent a general post.
    '''

    DEFAULT_PATH = os.path.expanduser(DATABASE_FILE)

    SQL_SELECT_UUID = 'SELECT * FROM Postdb WHERE uuid = ?'
    SQL_INSERT_POST = 'INSERT INTO Postdb (uuid, title, description, location, skill_set, num_volunteers, is_request, user_id, tags, volunteers, date, length) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    SQL_UPDATE_POST = 'UPDATE Postdb SET title=?, description=?, location=?, skill_set=?, num_volunteers=?, is_request=?, user_id=?, tags=?, volunteers=?, date=?, length=? WHERE uuid=?'
    SQL_DELETE_POST = 'DELETE from Postdb where uuid=?'
    SQL_GET_USER_POSTS = 'SELECT * FROM Postdb WHERE user_id = ?'

    SQL_CREATE_POST_TABLE = '''CREATE TABLE IF NOT EXISTS Postdb(
                uuid VARCHAR(100) PRIMARY KEY,
                title VARCHAR(100),
                description mediumtext,
                location VARCHAR(100),
                skill_set VARCHAR(200),
                num_volunteers int,
                is_request bool,
                user_id varchar(100),
                tags VARCHAR(200),
                volunteers VARCHAR(200),
                date DATE,
                length int
            )'''

    def __init__(self, title: str, description: str, location: str,
                 skill_set: List[str], num_volunteers: int, is_request: bool, user_id: int, tags: List[str] = None, volunteers: List[str] = None, date=None, length=None, uuid: str = ""):
        if not uuid:
            self.uuid = str(uuid1())
        else:
            self.uuid = uuid
        self.title = title
        self.description = description
        self.location = location
        self.skill_set = skill_set
        self.num_volunteers = num_volunteers
        self.is_request = is_request
        self.user_id = user_id
        self.tags = tags
        self.volunteers = []
        self.date = date
        self.length = length

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "skill_set": ','.join(self.skill_set),
            "num_volunteers": self.num_volunteers,
            "is_request": self.is_request,
            "user_id": self.user_id,
            "tags": ','.join(self.tags),
            "volunteers": self.volunteers
        }

    @classmethod
    def init_from_uid(cls, uuid: str = ""):
        """Initializes a new Post from the database, using the uuid"""
        if not uuid:
            return None

        conn = sqlite3.connect(Post.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Post.SQL_SELECT_UUID, (uuid,))
            data = curs.fetchone()
            if not data:
                return None
            return Post(data[1], data[2], data[3], data[4].split(','), data[5], data[6], data[7], data[8].split(',') if data[8] is not None else None, data[9], data[0])

    @classmethod
    def delete_from_uid(cls, uuid: str = "") -> None:
        """ Deletes a post from database based on uuid """
        if not uuid:
            return

        # open connection
        conn = sqlite3.connect(Post.DEFAULT_PATH)

        with conn:
            curs = conn.cursor()
            # perform delete
            curs.execute(Post.SQL_DELETE_POST, (uuid,))

    @classmethod
    def dump_table(cls) -> None:
        conn = sqlite3.connect(Post.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            print('------ Post -----')
            for row in curs.execute('SELECT * from Postdb'):
                print(row)
            print('--------------------')

    @classmethod
    def get_with_filter(cls, filter: dict):
        # build query
        query = 'SELECT * from Postdb'

        if 'type' in filter:
            if 'where' not in query:
                query += ' where '
            one_made = False
            for tag in filter['type']:
                print(tag)
                if one_made:
                    query += ' or '
                    one_made = True
                query += '{} like \'%{}%\''.format('tags', tag)
                one_made = True

        # return list
        print('performing query: {}'.format(query))
        Post.dump_table()

        conn = sqlite3.connect(DATABASE_FILE)
        with conn:
            curs = conn.cursor()
            return [Post.init_from_uid(row[0]).to_dict() for row in curs.execute(query)]

    @classmethod
    def init_table(cls) -> None:
        ''' Attempts to make SQL table if not already existing '''
        conn = sqlite3.connect(DATABASE_FILE)
        with conn:
            curs = conn.cursor()
            curs.execute(Post.SQL_CREATE_POST_TABLE)

    def insert_into_db(self) -> None:
        """ Inserts object into database """
        conn = sqlite3.connect(Post.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            # create tuple of input
            data = (self.uuid, self.title, self.description, self.location, ','.join(self.skill_set), self.num_volunteers, self.is_request,
                    self.user_id, ','.join(self.tags) if self.tags else None, ','.join(self.volunteers) if self.volunteers else None)
            # execute SQL insert
            curs.execute(Post.SQL_INSERT_POST, data)

    def update_in_db(self) -> None:
        """ Updates object in database """
        conn = sqlite3.connect(Post.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            # create input tuple to match SQL_UPDATE_POST's ? operators
            data = (self.title, self.description, self.location, ','.join(self.skill_set), self.num_volunteers, self.is_request,
                    self.user_id, ','.join(self.tags) if self.tags else None, ','.join(self.volunteers) if self.volunteers else None, self.uuid)
            # perform sql update
            curs.execute(Post.SQL_UPDATE_POST, data)

    def delete_in_db(self) -> None:
        """ Deletes object from database """
        conn = sqlite3.connect(Post.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            # call delete
            curs.execute(Post.SQL_DELETE_POST, (self.uuid, ))

    @classmethod
    def get_by_user_id(cls, user_id):
        """ Get all posts made by a user """
        conn = sqlite3.connect(Post.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            # call delete
            curs.execute(Post.SQL_GET_USER_POSTS, (user_id, ))
            return curs.fetchall()

    def get_uuid(self) -> str:
        ''' returns uuid '''
        return self.uuid

    def get_title(self) -> str:
        ''' returns title of post '''
        return self.title

    def set_title(self, title: str) -> str:
        ''' sets title of post '''
        self.title = title

    def get_description(self) -> str:
        ''' gets description of post '''
        return self.description

    def set_description(self, description: str) -> None:
        ''' sets description of post '''
        self.description = description

    def get_location(self) -> str:
        ''' gets location attached to post '''
        return self.location

    def set_location(self, location: str) -> None:
        ''' sets location of post '''
        self.location = location

    def get_skill_set(self) -> List[str]:
        ''' returns skill set attached to post '''
        return self.skill_set

    def set_skill_set(self, skill_set: List[str]) -> None:
        ''' sets skill set attached to post '''
        self.skill_set = skill_set

    def get_num_volunteers(self) -> int:
        ''' returns number of volunteers available/needed '''
        return self.num_volunteers

    def set_num_volunteers(self, num_volunteers: int):
        ''' sets number of volunteers needed/available '''
        self.num_volunteers = num_volunteers

    def get_is_request(self) -> bool:
        ''' return if the post is a request '''
        return self.is_request

    def set_is_request(self, is_request: bool) -> None:
        ''' sets if the post is a request '''
        self.is_request = is_request

    def get_tags(self) -> List[str]:
        ''' gets tags from post '''
        return self.tags

    def set_tags(self, tags: List[str]) -> None:
        ''' sets tags of post '''
        self.tags = tags

    def add_tag(self, tag: str) -> None:
        ''' add an additonal tag to post '''
        self.tags.append(tag)

    def get_volunteers(self) -> List[str]:
        return self.volunteers

    def set_volunteers(self, volunteers: List[str]) -> None:
        self.volunteers = volunteers

    def add_volunteer(self, acc_id: str) -> None:
        self.volunteers.append(acc_id)


if __name__ == '__main__':
    conn = sqlite3.connect(DATABASE_FILE)
    with conn:
        curs = conn.cursor()
        SQL_CREATE_POST_TABLE = '''CREATE TABLE IF NOT EXISTS Postdb(
                    uuid VARCHAR(100) PRIMARY KEY,
                    title VARCHAR(100),
                    description mediumtext,
                    location VARCHAR(100),
                    skill_set VARCHAR(200),
                    num_volunteers int,
                    is_request bool,
                    user_id varchar(100),
                    tags VARCHAR(200),
                    volunteers VARCHAR(200),
                    date DATE,
                    length int
                )'''

        curs.execute(SQL_CREATE_POST_TABLE)

        o = Post("test boinew", "desc", "loc", [
                 'technology'], 69, True, 'uid69420', ['technology'])
        o.insert_into_db()

        o2 = Post("2ndpost", "desc2l", "loc2", [
                  'technology'], 420, True, 'uid69420', ['technology', 'plumbing'])
        o2.insert_into_db()

        for row in curs.execute('SELECT * FROM Postdb'):
            print(row)

        o.set_num_volunteers(3)

        o.update_in_db()

        for row in curs.execute('SELECT * FROM Postdb'):
            print(row)

        res = Post.get_by_user_id("uid69420")
        print(res)

        print()
        for post in Post.get_with_filter({'tags': ['boi']}):
            print(post['tags'])
