# Account.py

from uuid import uuid1
import os
import sqlite3
from constants import DATABASE_FILE
from post import Post

from typing import List

class Account():
    '''
    Abstract class representing general account features
    '''

    DEFAULT_PATH = os.path.expanduser(DATABASE_FILE)

    SQL_SELECT_UUID = 'SELECT * FROM Account WHERE uuid = ?'
    SQL_INSERT_ACCOUNT = '''INSERT INTO Account VALUES(?, ?, ?, ?, ?, ?, ?)'''
    SQL_UPDATE_ACCOUNT = '''UPDATE Account SET name=?, email=?, password=?, is_personal=?, bio=?, phone=? WHERE uuid=?'''
    SQL_DELETE_ACCOUNT = 'DELETE FROM Account WHERE uuid = ?'

    SQL_SELECT_EMAIL = 'SELECT * FROM Account WHERE email = ?'
    SQL_CHECK_VALID = 'SELECT * FROM Account WHERE email = ? and password = ?'

    def __init__(self, name: str, email: str, password: str, is_personal: bool, bio: str=None, phone:str=None, uuid:str=""):
        # Uuid attached to Accoutn for identification
        self.uuid = str(uuid1()) if not uuid else uuid
        self.name = name
        self.email = email
        self.password = password
        self.is_personal = is_personal
        self.bio = bio
        self.phone = phone
    
    @classmethod
    def exists(self, email: str) -> bool:
        ''' check if account exists'''
        conn = sqlite3.connect(Account.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Account.SQL_SELECT_EMAIL, (email, ))
            # check if exists
            data = curs.fetchone()
            # return if account is there 
            return not (data is None)

    @classmethod
    def validate(self, email: str, passwd: str): # Returns object or none
        ''' return object if pass is match'''
        conn = sqlite3.connect(Account.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Account.SQL_CHECK_VALID, (email, passwd, ))
            # check if exists
            data = curs.fetchone()
            # return if account is there 
            return data

    @classmethod
    def init_from_uuid(cls, uuid: str): # returns object that represents Account
        """Initializes a new Person from the database, using the uuid"""
        if not uuid: return None
        conn = sqlite3.connect(Account.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Person.SQL_SELECT_UUID, (uuid,))

            # check if exists
            data = curs.fetchone()
            if not data: return None

            # dispatch to proper initializers
            if data[4]: return Person.init_from_uid(uuid)
            else:       return Organization.init_from_uid(uuid)

    def create_post(self, title: str, description: str, location: str,
            skill_set: List[str], num_volunteers: int, is_request: bool, tags: List[str] = None) -> None:
        ''' Creates post in DB at attaches it to user account '''
        new_post = Post(title, description, location, skill_set, num_volunteers, is_request, self.uuid, tags)
        new_post.insert_into_db()

    def get_name(self) -> str:
        ''' gets user name '''
        return self.name

    def set_name(self, new_name: str) -> None:
        ''' sets user name '''
        self.name = new_name

    def get_uuid(self) -> str:
        return self.uuid

    def get_email(self) -> str:
        ''' gets user email '''
        return self.email

    def set_email(self, new_email: str) -> None:
        ''' sets user email '''
        self.email = new_email

    def get_phone(self) -> str:
        ''' gets user phone '''
        return self.phone

    def set_phone(self, new_phone: str) -> None:
        ''' sets user phone '''
        self.phone = new_phone

    def get_bio(self) -> str:
        return self.bio

    def set_bio(self, new_bio: str) -> None:
        self.bio = new_bio


class Person(Account):
    '''in db: uuid, email, phone, name, bio, dob, skills'''

    DEFAULT_PATH = os.path.expanduser(DATABASE_FILE)

    SQL_SELECT_UUID = 'SELECT * FROM Person WHERE uuid = ?'
    SQL_INSERT_PERSON = '''INSERT INTO Person VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    SQL_UPDATE_PERSON = '''UPDATE Person SET name=?, dob=?, bio=?, email=?, phone=?, skills=?, password=? WHERE uuid=?'''
    SQL_DELETE_PERSON = 'DELETE FROM Person WHERE uuid = ?'

    def __init__(self, name: str, dob: str, email: str, password: str, bio: str=None, phone: str=None, skills: List[str]=None, uuid: str=""):
        super(Person, self).__init__(name, email, password, True, bio, email, phone, uuid)
        self.dob = dob
        self.skills = skills

    def get_dob(self) -> str:
        return self.dob

    def get_skills(self) -> List[str]:
        return self.skills

    def set_skills(self, new_skills: List[str]) -> None:
        self.skills = new_skills

    def insert_into_db(self) -> None:
        skills = ','.join([skill for skill in self.skills]) if self.skills else self.skills
        conn = sqlite3.connect(Person.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            ins_tuple = (self.uuid, self.email, self.password, self.phone, self.name, self.bio, self.dob, skills)
            curs.execute(Person.SQL_INSERT_PERSON, ins_tuple)


    def update_into_db(self) -> None:
        skills = ','.join([skill for skill in self.skills]) if self.skills else self.skills
        conn = sqlite3.connect(Person.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            ins_tuple = (self.email, self.phone, self.name, self.bio, self.dob, skills, self.uuid, self.password)
            curs.execute(Person.SQL_UPDATE_PERSON, ins_tuple)

    @classmethod
    def del_from_db(cls, uuid: str) -> None:
        uuid = str(uuid)
        conn = sqlite3.connect(Person.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Person.SQL_DELETE_PERSON, (uuid,))


    @classmethod
    def init_from_uid(cls, uuid: str="") -> None:
        """Initializes a new Person from the database, using the uuid"""
        if not uuid: return None

        conn = sqlite3.connect(Person.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Person.SQL_SELECT_UUID, (uuid,))
            data = curs.fetchone()
            if not data: return None
            return Person(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])


class Organization(Account):
    '''in db: uuid, email, phone, name, bio, industry'''

    DEFAULT_PATH = os.path.expanduser(DATABASE_FILE)

    SQL_SELECT_UUID = 'SELECT * FROM Organization WHERE uuid = ?'
    SQL_INSERT_ORG = 'INSERT INTO Organization VALUES(?, ?, ?, ?, ?, ?)'
    SQL_UPDATE_ORG = 'UPDATE Organization SET email=?, phone=?, name=?, bio=?, industry=? WHERE uuid=?'
    SQL_DELETE_ORG = 'DELETE FROM Organization WHERE uuid = ?'

    def __init__(self, industry, name, email, password, bio=None, phone=None, uuid: str=""):
        super(Organization, self).__init__(name, email, password, bio, phone, uuid)
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
                    password VARCHAR(100),
                    phone CHAR(10),
                    name VARCHAR(100),
                    bio TEXT,
                    dob DATE,
                    industry VARCHAR(100)
                )'''
        curs.execute(SQL_CREATE_PERSON_TABLE)
