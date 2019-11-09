# Post.py

import os

import sqlite3

from uuid import uuid1

class Post:
    '''
    Class to represent a general post.
    '''

    DEFAULT_PATH = os.path.expanduser('~../db')

    SQL_SELECT_UUID = 'SELECT * FROM Postdb WHERE uuid = ?'
    SQL_INSERT_POST = 'INSERT INTO Postdb (uuid, title, description, location, skill_set, num_volunteers, is_requests, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'


    def __init__(self, title: str, description: str, location: str,
            skill_set: List(str), num_volunteers: int, is_request: bool, tags=None: List(str)):
        self.uuid = str(uuid1())
        self.title = title
        self.description = description
        self.location = location
        self.skill_set = skill_set
        self.num_volunteers = num_volunteers
        self.is_request = is_request
        self.tags = tags

    @classmethod
    def init_from_uid(cls, uuid="": str) -> Post:
        """Initializes a new Post from the database, using the uuid"""
        if not uuid: return None
        
        conn = sqlite3.connect(Post.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Post.SQL_SELECT_UUID, (uuid,))
            data = curs.fetchone()
            if not data: return None
            return Post(data[0], data[1], data[2], data[3], data[4], data[5], data[6])

    def insert_in_db(self) -> None:
        conn = sqlite3.connect(Post.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            # create tuple of input
            data = (self.uuid, self.title, self.description, self.location, self.skill_set, self.num_volunteers, self.is_request, self.tags)
            # execute SQL insert
            curs.execute(Post.SQL_INSERT_POST, data)


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

    def get_skill_set(self) -> List(str):
        ''' returns skill set attached to post '''
        return self.skill_set

    def set_skill_set(self, skill_set: List(str)) -> None:
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

    def get_tags(self) -> List(str):
        ''' gets tags from post '''
        return self.tags

    def set_tags(self, tags: List(str)) -> None:
        ''' sets tags of post '''
        self.tags = tags

    def add_tag(self, tag: str) -> None:
        ''' add an additonal tag to post '''
        self.tags.append(tag)
