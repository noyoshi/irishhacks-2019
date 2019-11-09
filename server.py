import sys
import json

from flask import Flask, render_template, make_response, request
from backend.account import Person, Organization, Account
from backend.post import Post
from backend.token import TokenTable

sys.path.append('./frontend')
sys.path.append('./backend')

app = Flask(__name__)

TOKEN_NAME = "custom_token"
FAIL_MSG = json.dumps({"status": "failure"})

Person.init_table()
Account.init_table()
Organization.init_table()

def get_userid():
    token_conn = TokenTable()
    cookie = request.cookies.get("custom_token")
    print(cookie)
    user_id = token_conn.get_uuid(cookie)
    if not user_id or not token_conn.validate(user_id, cookie):
        print("INVALID_TOKEN: {}".format(cookie))
        return None
    
    return user_id

@app.route("/")
def index():
    # if they are logged in, they are going to have some small thing saying theya re looged in
    return render_template("main.html", token_uuid=get_userid())


@app.route("/about")
def about():
    # if they are logged in, they are going to have some small thing saying theya re looged in
    return render_template("about.html", token_uuid=get_userid())


@app.route("/help")
def help():
    # if they are logged in, they are going to have some small thing saying theya re looged in
    return render_template("help.html", token_uuid=get_userid())


# TODO needs authentication
@app.route("/edit/post/<postid>")
def edit_post(postid):
    post = Post.init_from_uid(postid)
    # TODO edit the post object
    # TODO save the post object
    return "edit post {}".format(postid)

@app.route("/handle_login", methods=["POST"])
def handle_login():
    # this handles the login
    # if login is success, return succcess
    # if login fails, return fail 
    fail = json.dumps({"status": "failure"})
    success = make_response(json.dumps({"status": "success"}))
    request_json = request.json
    
    if not request.json:
        return fail
    
    email = request_json.get("email")
    password = request_json.get("password")

    if not email:
        return json.dumps({"status": "failure", "issue": "no email"})
    
    if not password:
        return json.dumps({"status": "failure", "issue": "no password"})
    
    # otherwise, chceck to make sure email and password match
    # if they do, add cookie to success
    # if they do not, response with failure
    # TODO 

    # TODO while waiting for sam, assume they do match
    account = Account.validate(email, password)
    Account.dump_table()
    if not account:
        return json.dumps({"status": "failure", "issue": "invalid login / no account"})

    user_id = account.get_uuid()
    token_table = TokenTable()
    token_id = token_table.create(user_id)
    success.set_cookie(TOKEN_NAME, token_id)
    print("login success")

    return success


@app.route("/handle_signup", methods=["POST"])
def handle_signin():
    # this handles the login
    # if login is success, return succcess
    # if login fails, return fail 
    print(request.json)
    request_json = request.json

    fail = json.dumps({"status": "failure"})
    success = make_response(json.dumps({"status": "success"}))
    # request_json = json.loads(request.json)
    
    if not request.json:
        return fail
    
    email = request_json.get("email")
    password = request_json.get("password")
    name = request_json.get("name")

    if not email:
        return json.dumps({"status": "failure", "issue": "no email"})
    
    if not password:
        return json.dumps({"status": "failure", "issue": "no password"})
    
    if not name:
        return json.dumps({"status": "failure", "issue": "no name"})
    # TODO check to see if email exists in the db, if so, return failure

    if Account.exists(email):
        return json.dumps({"status": "failure", "issue": "email exists"})

    # TODO change for person vs org
    user = Person(name, 10, email, password)
    user.insert_into_db()
    # TODO set password

    user_id = user.get_uuid()
    token_table = TokenTable()
    token_id = token_table.create(user_id)
    success.set_cookie(TOKEN_NAME, token_id)
    return success

@app.route("/login")
def login():
    """
    email       (string)
    password    (string)
    """
    # we need to give the user a cookie, if they are not logged in, so that we can figure out if they are validated?
    # 1. if they are not logged in, then they are prompted to login
        # after login, they are given the uuid token
    # 2. if they login with an existing email and, check the password to see if it matches, it if does, they get the cookie with uuid
        # if the password does not match, they are again prompted to this page
    # TODO the login route should also have info about the route they were trying to go down before, so tif they are logged in / 
    # when they are logged in, it should send them to the right place
    
    cookie = request.cookies.get(TOKEN_NAME)

    # # no cookie
    if not cookie:
        return render_template("login.html")
    
    token_conn = TokenTable()
    user_id = token_conn.get_uuid(cookie)

    # malformed cookie
    if not user_id:
        return render_template("login.html")
    
    # # valid user_id expired token -> make a new token?
    if user_id and cookie and not token_conn.validate(user_id, cookie):
        return render_template("login.html")
    
    # user is logged in
    if user_id and cookie and token_conn.validate(user_id, cookie):
        user = Account.init_from_uuid(user_id)
        return render_template("login.html", logged_in=True, token_uuid=user_id, **user.to_dict())
    
    print("error?")
    return render_template("login.html")


@app.route("/signup")
def signup():
    """
    email    (string)
    password (string) **not hashed yet!
    """
    # similar to the login route
    
    cookie = request.cookies.get(TOKEN_NAME)

    # # no cookie
    if not cookie:
        return render_template("signup.html")
    
    token_conn = TokenTable()
    user_id = token_conn.get_uuid(cookie)
    account = Account.init_from_uuid(user_id)

    # if they are logge din with valid cookie
    if user_id and cookie and token_conn.validate(user_id, cookie):
        return render_template("signup.html", token_uuid=get_userid(), logged_in=True, **account.to_dict())
    
    return render_template("signup.html")


# TODO if they are logged in, they can respond to the post
@app.route("/posts")
def posts():
    """
    we are going to have some filtering going on...
    """
    # if they are logged in, they are going to have a small thing saying they are logged in
    return render_template("posts.html", token_uuid=get_userid())


@app.route("/community")
def community():
    """
    returns a list of the people in the community!
    """
    return render_template("community.html", token_uuid=get_userid())

@app.route("/profile/<userid>")
def user_profile(userid):
    """
    userid (string)
    first_name (string)
    last_name (string)
    phone_number (number)
    email (string)
    """
    # if they are logged in, they are going to have some small thing saying theya re looged in
    account = Account.init_from_uuid(userid)
    if not account:
        return "no profile"
    return render_template("profile.html", token_uuid=get_userid(), **account.to_dict())


# TODO needs authentication
@app.route("/profile/edit/<userid>")
def edit_profile(userid):
    token_user_id = get_userid()
    
    if token_user_id != userid:
        print("ERROR CANNOT EDIT ANOTHER USERS PAGE")
        return "error cannot edit another persons user page"

    account = Account.init_from_uuid(userid)
    if not account:
        print("Nontype account for token user id {} and userid {}".format(token_user_id, userid))
        return render_template("login.html")
    if isinstance(type(Person), type(account)):
        # we are a person
        pass
    else:
        # we are an org
        pass
    # TODO edit the person object
    # TODO save the person object
    return render_template("edit_profile.html", token_uuid=token_user_id, **account.to_dict())


@app.route("/profile/save_edits", methods=["POST"])
def save_profile_edits():
    """Saves the profile edits that we get from the user"""
    token_user_id = get_userid()
    if not token_user_id:
        # expired token
        return FAIL_MSG
    
    account = Account.init_from_uuid(token_user_id)
    if not account:
        return FAIL_MSG

    data = request.json
    if "firstname" or "lastname" in data:
        if not data["firstname"] and not data["lastname"]:
            pass
        else:
            account.set_name(data.get("firstname", "") + " " + data.get("lastname", ""))
    

    if "email" in data and data["email"]:
        account.set_email(data["email"])
    
    if "bio" in data and data["bio"]:
        account.set_bio(data["bio"])

    if "dob" in data and data["dob"]:
        if isinstance(type(account), type(Person)):
            account.set_dob(data["dob"])

    if "phone_number" in data and data["phone_number"]:
        account.set_phone(data["phone_number"])
    
    account.update_into_db()

    Person.dump_table()
    return json.dumps({ 
        "status": "success", 
        "uuid": account.get_uuid()
    })
    # make sure to return something with the uuid in it!


@app.route("/post/save_edits", methods=["POST"])
def save_post_edits():
    """Saves the post edits that we got form the user"""
    pass


@app.route("/posts/handle_post_filter", methods=["POST"])
def get_filtered_posts():
    ''' not actually posting anything lol '''
    print(request.json)
    return json.dumps({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='41001')
