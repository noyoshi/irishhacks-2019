from flask import Blueprint, render_template, request, make_response
from utils import get_userid, TOKEN_NAME, FAIL_MSG
from backend.account import Account, Person, Organization
from backend.token import TokenTable
import json

auth_api = Blueprint('auth_api', __name__)


@auth_api.route("/handle_login", methods=["POST"])
def handle_login():
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


@auth_api.route("/handle_signup", methods=["POST"])
def handle_signin():
    request_json = request.json

    fail = json.dumps({"status": "failure"})
    success = make_response(json.dumps({"status": "success"}))

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


@auth_api.route("/login")
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


@auth_api.route("/signup")
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
