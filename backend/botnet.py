## HACK INTO DATABASE

import random
from account import Person, Account
from post import Post

NAMES = ('billy', 'bob', 'boi', 'bill theisen', 'noah', 'yoshida', 'bui')
EMAIL = ('b@b.com', 'yeet@boi.com', 'bill@theisen.com', 'pbui@nd.edu')
PASS = ('pass', 'word', '1234', 'swag', 'corkbor')
IS_PERS = (True, False)
BIO  = ('hey there', 'bo', 'yay ya ya ya ', 'oy oy oy oy', 'description')
PHONE = ('574-8675-309', '69696969696', 'phone', '123-456-7890')
ADDR  = ('123 fake street', '200 alumni hall', '1600 pennsylvania av.')
skills = (['dank'], ['test'])

def dummy_user():
    return Person(random.choice(NAMES),random.choice(EMAIL), random.choice(PASS),  '6969', random.choice(BIO),
                  random.choice(PHONE), random.choice(ADDR), random.choice(skills))


TITLE = ('help me change my tire', 'i\'ve fallen and i can\'t get up', 'my water heater broke pls help')
DESC  = ('Could a nice person help me with my above problem?', 'Please help this is urgent!!', 'Any help or suggestions would be appreciated!')
LOC   = ('South Bend', 'Notre Dame', 'Gary', 'Chicago', 'Washington', 'Mountainview')
SKILL_SET = (['manual labor'], ['electricity'], ['plumbing'])
NUM_VOLS = (1,2,3,4,5,6,7)
IS_REQ = (True, False)
TAGS = (['electrician'], ['plumbing'], ['technology'], ['handyman'], ['general'], ['other'])
DATE = ('02/25/1999', '60/34/1203', '01/10/1923')
LEN  = (0,1,2,4,5,6,7,8)


def create_post(user: Person):
    user.create_post(random.choice(TITLE), random.choice(DESC), random.choice(LOC), random.choice(SKILL_SET), random.choice(NUM_VOLS),
    random.choice(IS_REQ), random.choice(TAGS), random.choice(DATE), random.choice(LEN))

if __name__ == '__main__':
    Account.init_table()
    Person.init_table()
    Post.init_table()

    for i in range(10):
        user = dummy_user()
        user.insert_into_db()
        create_post(user)
    Account.dump_table()
    Person.dump_table()
    Post.dump_table()