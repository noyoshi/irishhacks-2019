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
    SQL_INSERT_ACCOUNT = '''INSERT INTO Account VALUES(?, ?, ?, ?, ?, ?, ?, ?)'''
    SQL_UPDATE_ACCOUNT = '''UPDATE Account SET name=?, email=?, password=?, is_personal=?, bio=?, phone=?, address=? WHERE uuid=?'''
    SQL_DELETE_ACCOUNT = 'DELETE FROM Account WHERE uuid = ?'

    SQL_SELECT_EMAIL = 'SELECT * FROM Account WHERE email = ?'
    SQL_CHECK_VALID = 'SELECT * FROM Account WHERE email = ? and password = ?'

    SQL_CREATE_ACCOUNT_TABLE = '''CREATE TABLE IF NOT EXISTS Account(
            uuid VARCHAR(100) PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            password VARCHAR(100),
            is_personal bool,
            bio TEXT,
            phone CHAR(10),
            address VARCHAR(100) 
        )'''

    def __init__(self, name: str, email: str, password: str, is_personal: bool, bio: str=None, phone:str=None, address:str=None, uuid:str=""):
        # Uuid attached to Accoutn for identification
        if not uuid:
            print("ACCOUNT CREATED")
        self.uuid = str(uuid1()) if not uuid else uuid
        self.name = name
        self.email = email
        self.password = password
        self.is_personal = is_personal
        self.bio = bio
        self.phone = phone
        self.address = address
    
    def to_dict(self):
        return {
            "name": self.name, 
            "email": self.email,
            "is_personal": self.is_personal,
            "bio": self.bio, 
            "phone": self.phone,
            "address": self.address,
            "uuid": self.uuid
        }
    
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
            if not data:
                return None
            return Account.init_from_uuid(data[0])

    @classmethod
    def init_from_uuid(cls, uuid: str): # returns object that represents Account
        """Initializes a new Person from the database, using the uuid"""
        if not uuid: return None
        conn = sqlite3.connect(Account.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Account.SQL_SELECT_UUID, (uuid,))

            # check if exists
            data = curs.fetchone()
            if not data: return None
            print(data)
            # dispatch to proper initializers
            if data[4]: return Person.init_from_uid(uuid, data)
            else:       return Organization.init_from_uid(uuid, data)
    
    @classmethod
    def del_from_db(cls, uuid: str) -> None:
        uuid = str(uuid)
        conn = sqlite3.connect(Account.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Account.SQL_DELETE_ACCOUNT, (uuid,))
    
    @classmethod
    def dump_table(cls) -> None:
        conn = sqlite3.connect(Account.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            print('------ Account -----')
            for row in curs.execute('SELECT * from Account'):
                print(row)
            print('--------------------')
    
    @classmethod
    def init_table(cls) -> None:
        ''' Attempts to make SQL table if not already existing '''
        conn = sqlite3.connect(DATABASE_FILE)
        with conn:
            curs = conn.cursor()
            curs.execute(Account.SQL_CREATE_ACCOUNT_TABLE)
    
    def insert_into_db(self) -> None:
        conn = sqlite3.connect(Account.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            ins_tuple = (self.uuid, self.name, self.email, self.password, self.is_personal, self.bio, self.phone, self.address)
            curs.execute(Account.SQL_INSERT_ACCOUNT, ins_tuple)

    def update_into_db(self) -> None:
        conn = sqlite3.connect(Account.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            ins_tuple = (self.name, self.email, self.password, self.is_personal, self.bio, self.phone, self.address, self.uuid)
            curs.execute(Account.SQL_UPDATE_ACCOUNT, ins_tuple)

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
    
    def get_address(self) -> str:
        return self.address
    
    def set_address(self, address: str) -> None:
        self.address = address


class Person(Account):
    '''in db: uuid, email, phone, name, bio, dob, skills'''

    DEFAULT_PATH = os.path.expanduser(DATABASE_FILE)

    SQL_SELECT_UUID = 'SELECT * FROM Person WHERE uuid = ?'
    SQL_INSERT_PERSON = '''INSERT INTO Person VALUES(?, ?, ?)'''
    SQL_UPDATE_PERSON = '''UPDATE Person SET dob=?, skills=? WHERE uuid=?'''
    SQL_DELETE_PERSON = 'DELETE FROM Person WHERE uuid = ?'

    SQL_CREATE_PERSON_TABLE = '''CREATE TABLE IF NOT EXISTS Person(
        uuid VARCHAR(100) PRIMARY KEY,
        dob DATE,
        skils VARCHAR(100)
    )'''


    def __init__(self, name: str, dob: str, email: str, password: str, bio: str=None, phone: str=None, address: str=None, skills: List[str]=None, uuid: str=""):
        super(Person, self).__init__(name, email, password, True, bio, phone, address, uuid)
        self.dob = dob
        self.skills = skills
    
    def to_dict(self):
        d = super().to_dict()
        # d["dob"] = self.dob
        # d["skills"] = self.skills
        return d

    @classmethod
    def del_from_db(cls, uuid: str) -> None:
        ''' deletes from both db's based on uuid '''
        super().del_from_db(uuid)
        conn = sqlite3.connect(Person.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Person.SQL_DELETE_PERSON, (uuid,))

    @classmethod
    def init_from_uid(cls, uuid: str="", data: List[str]=None) -> None:
        """Initializes a new Person from the database, using the uuid"""
        if not uuid: return None

        conn = sqlite3.connect(Person.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Person.SQL_SELECT_UUID, (uuid,))
            per_data = curs.fetchone()
            if not per_data: return None
            return Person(data[1], per_data[1], data[2], data[3], data[5], data[6], data[7], ','.join(per_data[2]) if per_data[2] else None, data[0])

    @classmethod
    def init_table(cls) -> None:
        ''' Attempts to make SQL table if not already existing '''
        conn = sqlite3.connect(DATABASE_FILE)
        with conn:
            curs = conn.cursor()
            curs.execute(Person.SQL_CREATE_PERSON_TABLE)

    @classmethod
    def dump_table(cls) -> None:
        conn = sqlite3.connect(Person.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            print('------ Person -----')
            for row in curs.execute('SELECT * from Person'):
                print(row)
            print('--------------------')

    def get_dob(self) -> str:
        return self.dob

    def get_skills(self) -> List[str]:
        return self.skills

    def set_skills(self, new_skills: List[str]) -> None:
        self.skills = new_skills

    def insert_into_db(self) -> None:
        super().insert_into_db()
        skills = ','.join([skill for skill in self.skills]) if self.skills else self.skills
        conn = sqlite3.connect(Person.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            ins_tuple = (self.uuid, self.dob, skills)
            curs.execute(Person.SQL_INSERT_PERSON, ins_tuple)


    def update_into_db(self) -> None:
        super(Person, self).update_into_db()
        skills = ','.join([skill for skill in self.skills]) if self.skills else self.skills
        conn = sqlite3.connect(Person.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            ins_tuple = (self.uuid, self.dob, self.skills)
            curs.execute(Person.SQL_UPDATE_PERSON, ins_tuple)


class Organization(Account):
    '''in db: uuid, email, phone, name, bio, industry'''

    DEFAULT_PATH = os.path.expanduser(DATABASE_FILE)

    SQL_SELECT_UUID = 'SELECT * FROM Organization WHERE uuid = ?'
    SQL_INSERT_ORG = 'INSERT INTO Organization VALUES(?, ?)'
    
    SQL_UPDATE_ORG = 'UPDATE Organization SET industry=? WHERE uuid=?'
    SQL_DELETE_ORG = 'DELETE FROM Organization WHERE uuid = ?'

    SQL_CREATE_ORG_TABLE = '''CREATE TABLE IF NOT EXISTS Organization(
        uuid VARCHAR(100) PRIMARY KEY,
        industry VARCHAR(100)
    )'''


    def __init__(self, name: str, email: str, password: str, bio: str=None, phone: str=None, address: str=None, industry: str="", uuid: str=""):
        super(Organization, self).__init__(name, email, password, bio, phone, address, uuid)
        self.industry = industry
    
    def to_dict(self):
        d = super().to_dict()
        d["industry"] = self.industry
        return d

    def get_industry(self):
        return self.industry


    def set_industry(self, new_industry):
        self.industry = new_industry


    def update_into_db(self):
        super(Organization, self).update_into_db()
        conn = sqlite3.connect(Organization.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            ins_tuple = (self.industry, self.uuid)
            curs.execute(Organization.SQL_UPDATE_ORG, ins_tuple)


    def insert_into_db(self):
        super(Organization, self).insert_into_db()
        conn = sqlite3.connect(Organization.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            ins_tuple = (self.uuid, self.industry)
            curs.execute(Organization.SQL_INSERT_ORG, ins_tuple)


    @classmethod
    def del_from_db(cls, uuid: str) -> None:
        super().del_from_db(uuid) # call super
        conn = sqlite3.connect(Organization.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Organization.SQL_DELETE_ORG, (uuid,))


    @classmethod
    def init_from_uid(cls, uuid="", data: List[str]=None):
        """Initializes a new Post from the database, using the uuid"""
        if not uuid: return None

        conn = sqlite3.connect(Organization.DEFAULT_PATH)
        with conn:
            curs = conn.cursor()
            curs.execute(Organization.SQL_SELECT_UUID, (uuid,))
            org_data = curs.fetchone()
            if not org_data: return None
            return Organization(data[1], data[2], data[3], data[5], data[6], data[7], org_data[1], data[0])
    
    @classmethod
    def init_table(cls) -> None:
        ''' Attempts to make SQL table if not already existing '''
        conn = sqlite3.connect(DATABASE_FILE)
        with conn:
            curs = conn.cursor()
            curs.execute(Organization.SQL_CREATE_ORG_TABLE)

if __name__ == '__main__':
    conn = sqlite3.connect(DATABASE_FILE)
    with conn:
        curs = conn.cursor()
        SQL_CREATE_ACCOUNT_TABLE = '''CREATE TABLE IF NOT EXISTS Account(
                    uuid VARCHAR(100) PRIMARY KEY,
                    email VARCHAR(100),
                    password VARCHAR(100),
                    is_personal bool,
                    phone CHAR(10),
                    name VARCHAR(100),
                    bio TEXT
                )'''
        curs.execute(SQL_CREATE_ACCOUNT_TABLE)

        SQL_CREATE_ORG_TABLE = '''CREATE TABLE IF NOT EXISTS Organization(
            uuid VARCHAR(100) PRIMARY KEY,
            industry VARCHAR(100)
        )'''

        curs.execute(SQL_CREATE_ORG_TABLE)

        SQL_CREATE_PERSON_TABLE = '''CREATE TABLE IF NOT EXISTS Person(
            uuid VARCHAR(100) PRIMARY KEY,
            dob DATE,
            skils VARCHAR(100)
        )'''

        curs.execute(SQL_CREATE_PERSON_TABLE)
    
        test_account = Organization("bob", "bob@test", "1234password", "i make money", "574-222-2222", "money makers")

        test_account.insert_into_db()

        for row in curs.execute('SELECT * FROM Account'):
            print(row)


        for row in curs.execute('SELECT * from organization'):
            print(row)

        test_other = Person("joe", "02/25/1999", "yeet@boi.com","1233yeet","a man who likes to bool", "574-030-3039", None)

        test_other.insert_into_db()

        for row in curs.execute('SELECT * FROM Account'):
            print(row)


        for row in curs.execute('SELECT * from Person'):
            print(row)

        Account.dump_table()