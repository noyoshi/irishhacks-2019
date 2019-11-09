class contact_info:
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
