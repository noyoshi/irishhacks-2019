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


    def __init__(self, title, description, location,
                 skill_set, num_volunteers, is_request, tags=None):
        self.uuid = str(uuid1())
        self.title = title
        self.description = description
        self.location = location
        self.skill_set = skill_set
        self.num_volunteers = num_volunteers
        self.is_request = is_request
        self.tags = tags

    @classmethod
    def init_from_uid(uuid=""):
        """Initializes a new Post from the database, using the uuid"""
        if not uuid: return None
        
        conn = sqlite3.connect(Post.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Post.SQL_SELECT_UUID, (uuid,))
            data = curs.fetchone()
            if not data: return None
            return Post(data[0], data[1], data[2], data[3], data[4], data[5], data[6])

    def get_uuid(self):
        return self.uuid

    def get_title(self):
        ''' returns title of post '''
        return self.title

    def set_title(self, title):
        ''' sets title of post '''
        self.title = title

    def get_description(self):
        ''' gets description of post '''
        return self.description

    def set_description(self, description):
        ''' sets description of post '''
        self.description = description

    def get_location(self):
        ''' gets location attached to post '''
        return self.location

    def set_location(self, location):
        ''' sets location of post '''
        self.location = location

    def get_skill_set(self):
        ''' returns skill set attached to post '''
        return self.skill_set

    def set_skill_set(self, skill_set):
        ''' sets skill set attached to post '''
        self.skill_set = skill_set

    def get_num_volunteers(self):
        ''' returns number of volunteers available/needed '''
        return self.num_volunteers
    
    def set_num_volunteers(self, num_volunteers):
        ''' sets number of volunteers needed/available '''
        self.num_volunteers = num_volunteers

    def get_is_request(self):
        ''' return if the post is a request '''
        return self.is_request

    def set_is_request(self, is_request):
        ''' sets if the post is a request '''
        self.is_request = is_request

    def get_tags(self):
        ''' gets tags from post '''
        return self.tags

    def set_tags(self, tags):
        ''' sets tags of post '''
        self.tags = tags

    def add_tag(self, tag):
        ''' add an additonal tag to post '''
        self.tags.append(tag)
