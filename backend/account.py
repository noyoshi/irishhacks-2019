# Account.py

from uuid import uuid1

class Contact:
    def __init__(self, name, email=None, phone=None):
        self.name = name
        self.email = email
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

class Person:
    def __init__(self, dob, skills=None):
        self.dob = dob
        self.skills = skills

    def get_dob(self):
        return self.dob

    def get_skills(self):
        return self.skills
        
    def set_skills(self, new_skills):
        self.skills = new_skills
    
class Account:
    def __init__(self, Contact, 