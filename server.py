import sys
import json

from flask import Flask, render_template, make_response, request, redirect, url_for
from backend.account import Person, Organization, Account
from backend.post import Post
from backend.token import TokenTable
from hashlib import md5
from github import Github

sys.path.append('./frontend')
sys.path.append('./backend')

app = Flask(__name__)

TOKEN_NAME = "custom_token"
FAIL_MSG = json.dumps({"status": "failure"})

Person.init_table()
Account.init_table()
Organization.init_table()
Post.init_table()

# init github
g = Github("0818ef5d2eb1541a675ceca441eca6bd4e450623")
repo = g.get_repo("noyoshi/irishhacks-2019")

def get_userid():
    token_conn = TokenTable()
    cookie = request.cookies.get("custom_token")
    print(cookie)
    user_id = token_conn.get_uuid(cookie)
    if not user_id or not token_conn.validate(user_id, cookie):
        print("INVALID_TOKEN: {}".format(cookie))
        return None

    return user_id


def find_distance(location):
    ''' returns mile distance between current user's locaiton and the target location '''
    from geopy.geocoders import Nominatim
    from geopy.distance import great_circle
    geolocator = Nominatim(user_agent="volunteersite")
    user_location = geolocator.geocode(
        Account.init_from_uuid(get_userid).address)
    post_location = geolocator.geocode(location)
    return great_circle((user_location.latitude, user_location.longitude), (post_location.latitude, post_location.longitude)).miles


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

@app.route("/post_help", methods=["POST"])
def post_issue():
    '''
    expects this json
    {
    name: "Name",
    comment: "comment_text"
    }
    '''
    # name = request.args['name']
    # comment = request.args['comment']
    # data.form['name']
    # print(request.form.get('comment'))
    comment = request.form.get('comment')
    name = request.form.get('name')
    # print(request.form.get('name'))
    # print(comment)
    # name = data['name']
    # comment = data['comment']
    repo.create_issue(title='Question by {}'.format(name), body=comment)
    open_issues = repo.get_issues(state='open')
    return render_template("end_feedback.html", name=name)


@app.route("/make_post")
def new_post():
    return render_template("edit_post.html", token_uuid=get_userid())

# TODO needs authentication
@app.route("/edit/post/<postid>")
def edit_post(postid):
    post = Post.init_from_uid(postid)
    # TODO edit the post object
    # TODO save the post object
    return render_template("edit_post.html")


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
    is_user = request_json.get("is_user")
    print("is user", is_user)

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
    ClassToUse = Person if is_user else Organization
    user = ClassToUse(name, email, password)
    user.insert_into_db()

    if isinstance(type(Person), type(ClassToUse)):
        print("made a person")
    elif isinstance(type(Organization), type(ClassToUse)):
        print("made an org")
    else:
        print("probs an error when crating an entity")
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
        d = user.to_dict() if user else {}
        print("user_id: {}".format(user_id))
        return render_template("login.html", logged_in=True, token_uuid=user_id, **d)

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

    filter = {}
    if request.args and 'type' in request.args:
        print(request.args)
        filter['type'] = [request.args['type'].lower()]

    filtered = Post.get_with_filter(filter)

    # Add the personal thing in to the dict
    new_list = []
    for post_dict in filtered:
        uuid = post_dict["user_id"]
        user = Account.init_from_uuid(uuid)
        if user:
            post_dict["personal"] = 1 if user.is_personal else 2
            print("found")
            new_list.append(post_dict)
        else:
            print("not found", post_dict.items())

    return render_template("posts.html", token_uuid=get_userid(), posts=new_list)

# TODO if they are logged in, they can respond to the post
@app.route("/posts/add_to_post")
def add_to_posts():
    """
    we are going to have some filtering going on...
    """

    # get post id from request, create post object, add a volunteer to the post object, update
    post_id = request.json.post_id
    post = Post.init_from_uid(post_id)
    uuid = get_userid()
    post.add_volunteer(uuid)
    post.update_in_db()

    return render_template("posts.html", token_uuid=get_userid())


@app.route("/posts/<post_id>")
def view_post(post_id):
    """
    we are going to have some filtering going on...
    """

    # get post id from request, create post object, add a volunteer to the post object, update
    print('in view')
    post = Post.init_from_uid(post_id)
    if not post:
        return render_template("post.html")

    return render_template("post.html", **post.to_dict())


@app.route("/posts/create/")
def create_post_view():

    return render_template("edit_post.html")


@app.route("/posts/create_new/", methods=["POST"])
def create_new_post():
    cookie = request.cookies.get(TOKEN_NAME)

    # # no cookie
    if not cookie:
        return json.dumps({"status": "failure"})

    token_conn = TokenTable()
    user_id = token_conn.get_uuid(cookie)
    acc = Account.init_from_uuid(user_id)

    res = request.json
    post = acc.create_post(res['title'], res['description'], res['location'], res['skillset'],
                           res['num_volunteers'], True, res['tags'], [], res['start_date'], res['duration'])
    post = post.to_dict()
    post['status'] = 'success'

    return json.dumps(post)


@app.route("/logout")
def logout():
    response = make_response(render_template("main.html"))
    response.set_cookie(TOKEN_NAME, "")
    return response


@app.route("/community")
def community():
    """
    returns a list of the people in the community!
    """
    accounts = Account.get_all_accounts()

    account_dicts = []
    for account in accounts:
        if account is None:
            continue
        user = Account.init_from_uuid(account.get_uuid())
        if not user:
            continue
        d = user.to_dict()

        hashed_email = md5(user.get_email().encode('utf-8')).hexdigest()
        d["hashed_email"] = hashed_email
        account_dicts.append(d)

    return render_template("community.html", token_uuid=get_userid(), accounts=account_dicts)


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
    hashed_email = md5(account.get_email().encode('utf-8')).hexdigest()
    print(hashed_email)
    if not account:
        return "no profile"
    return render_template("profile.html", token_uuid=get_userid(), **account.to_dict(), email_hash=hashed_email)


# TODO needs authentication
@app.route("/profile/edit/<userid>")
def edit_profile(userid):
    token_user_id = get_userid()

    if token_user_id != userid:
        print("ERROR CANNOT EDIT ANOTHER USERS PAGE")
        return "error cannot edit another persons user page"

    account = Account.init_from_uuid(userid)
    if not account:
        print("Nontype account for token user id {} and userid {}".format(
            token_user_id, userid))
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
            account.set_name(data.get("firstname", "") +
                             " " + data.get("lastname", ""))

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

    # Handle distance filter by user's location
    req = request.json
    print(request.json)

    posts = []

    if req['type'] != 'Type':
        posts += Post.get_with_filter({'type': req['type']})

    if req['maxdist'] != 'Distance':
        pass
    return json.dumps({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='41001')
