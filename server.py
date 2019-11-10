import sys
import json

from flask import Flask,  make_response, request, redirect, url_for
from backend.account import Person, Organization, Account
from backend.post import Post
from backend.token import TokenTable
from hashlib import md5
from github_help import github_api
from post_routes import post_api
from authentication import auth_api
import os
from utils import get_userid, TOKEN_NAME, FAIL_MSG, render_template

# app.py
# profile.py
#  --> from app import app, request
sys.path.append('./frontend')
sys.path.append('./backend')

app = Flask(__name__)


Person.init_table()
Account.init_table()
Organization.init_table()
Post.init_table()

app.register_blueprint(github_api)
app.register_blueprint(post_api)
app.register_blueprint(auth_api)


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
    return render_template("main.html")


@app.route("/about")
def about():
    # if they are logged in, they are going to have some small thing saying theya re looged in
    return render_template("about.html")


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

    posts = Post.get_by_user_id(userid)
    _posts = []
    for p in posts:
        if p:
            d = {"volunteers": []}
            # _posts.append(p.to_dict())
            o = p.get_volunteers()
            if not o:
                continue
            for volunteer in p.get_volunteers():
                acc = Account.init_from_uuid(volunteer)
                d["volunteers"].append(acc.to_dict())
            _posts.append(d)
    print(_posts)
    return render_template("profile.html", token_uuid=get_userid(), **account.to_dict(), email_hash=hashed_email, posts=_posts)


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
    # from profile import *
    app.run(debug=True, host='127.0.0.1', port='41001')
