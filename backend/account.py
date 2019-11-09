# Account.py

from uuid import uuid1
import os
import sqlite3
from constants import DATABASE_FILE

class Account():

    def __init__(self, name, bio=None, email=None, phone=None):
        self.name = name
        self.uuid = str(uuid1())
        self.email = email
        self.bio = bio
        self.phone = phone


    def get_name(self):
        ''' gets user name '''
        return self.name


    def set_name(self, new_name):
        ''' sets user name '''
        self.name = new_name


    def get_uuid(self):
        return self.uuid


    def get_email(self):
        ''' gets user email '''
        return self.email


    def set_email(self, new_email):
        ''' sets user email '''
        self.email = new_email


    def get_phone(self):
        ''' gets user phone '''
        return self.phone


    def set_phone(self, new_phone):
        ''' sets user phone '''
        self.phone = new_phone


    def get_bio(self):
        return self.bio


    def set_bio(self, new_bio):
        self.bio = new_bio


class Person(Account):
    '''in db: uuid, email, phone, name, bio, dob, skills'''

    DEFAULT_PATH = os.path.expanduser(DATABASE_FILE)

    SQL_SELECT_UUID = 'SELECT * FROM Person WHERE uuid = ?'
    SQL_INSERT_PERSON = '''INSERT INTO Person VALUES(?, ?, ?, ?, ?, ?, ?)'''
    SQL_UPDATE_PERSON = '''UPDATE Person SET name=?, dob=?, bio=?, email=?, phone=?, skills=? WHERE uuid=?'''
    SQL_DELETE_PERSON = 'DELETE FROM Person WHERE uuid = ?'


    def __init__(self, name, dob, bio=None, email=None, phone=None, skills=None):
        super(Person, self).__init__(name, bio, email, phone)
        self.dob = dob
        self.skills = skills


    def get_dob(self):
        return self.dob


    def get_skills(self):
        return self.skills


    def set_skills(self, new_skills):
        self.skills = new_skills


    def insert_into_db(self):
        skills = ','.join([skill for skill in self.skills]) if self.skills else self.skills
        conn = sqlite3.connect(Organization.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            ins_tuple = (self.uuid, self.email, self.phone, self.name, self.bio, self.dob, skills)
            curs.execute(Person.SQL_INSERT_PERSON, ins_tuple)


    def update_into_db(self):
        skills = ','.join([skill for skill in self.skills]) if self.skills else self.skills
        conn = sqlite3.connect(Organization.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            ins_tuple = (self.email, self.phone, self.name, self.bio, self.dob, skills, self.uuid)
            curs.execute(Person.SQL_UPDATE_PERSON, ins_tuple)

    @classmethod
    def del_from_db(cls, uuid):
        uuid = str(uuid)
        conn = sqlite3.connect(Organization.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Person.SQL_DELETE_PERSON, (uuid,))


    @classmethod
    def init_from_uid(cls, uuid=""):
        """Initializes a new Person from the database, using the uuid"""
        if not uuid: return None

        conn = sqlite3.connect(Person.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Person.SQL_SELECT_UUID, (uuid,))
            data = curs.fetchone()
            if not data: return None
            return Person(data[0], data[1], data[2], data[3], data[4], data[5])


class Organization(Account):
    '''in db: uuid, email, phone, name, bio, industry'''

    DEFAULT_PATH = os.path.expanduser(DATABASE_FILE)

    SQL_SELECT_UUID = 'SELECT * FROM Organization WHERE uuid = ?'
    SQL_INSERT_ORG = 'INSERT INTO Organization VALUES(?, ?, ?, ?, ?, ?)'
    SQL_UPDATE_ORG = 'UPDATE Organization SET email=?, phone=?, name=?, bio=?, industry=? WHERE uuid=?'
    SQL_DELETE_ORG = 'DELETE FROM Organization WHERE uuid = ?'


    def __init__(self, industry, name, bio=None, email=None, phone=None):
        super(Organization, self).__init__(name, bio, email, phone)
        self.industry = industry


    def get_industry(self):
        return self.industry


    def set_industry(self, new_industry):
        self.industry = new_industry


    def update_into_db(self):
        conn = sqlite3.connect(Organization.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            ins_tuple = (self.email, self.phone, self.name, self.bio, self.industry, self.uuid)
            curs.execute(Organization.SQL_UPDATE_ORG, ins_tuple)


    def insert_into_db(self):
        conn = sqlite3.connect(Organization.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            ins_tuple = (self.uuid, self.email, self.phone, self.name, self.bio, self.industry)
            curs.execute(Organization.SQL_INSERT_ORG, ins_tuple)


    @classmethod
    def del_from_db(cls, uuid):
        uuid = str(uuid)
        conn = sqlite3.connect(Organization.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Organization.SQL_DELETE_ORG, (uuid,))


    @classmethod
    def init_from_uid(cls, uuid=""):
        """Initializes a new Post from the database, using the uuid"""
        if not uuid: return None

        conn = sqlite3.connect(Organization.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Organization.SQL_SELECT_UUID, (uuid,))
            data = curs.fetchone()
            if not data: return None
            return Organization(data[0], data[1], data[2], data[3], data[4])


if __name__ == '__main__':
    conn = sqlite3.connect(DATABASE_FILE)
    with conn:
        curs = conn.cursor()
        SQL_CREATE_PERSON_TABLE = '''CREATE TABLE IF NOT EXISTS Organization(
                    uuid VARCHAR(100) PRIMARY KEY,
                    email VARCHAR(100),
                    phone CHAR(10),
                    name VARCHAR(100),
                    bio TEXT,
                    industry VARCHAR(100)
                )'''

        curs.execute(SQL_CREATE_PERSON_TABLE)
