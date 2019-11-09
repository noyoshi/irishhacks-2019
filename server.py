import sys
from flask import Flask, render_template

sys.path.append('../frontend')

app = Flask(__name__)

@app.route("/")
def index():
    return 'Welcome to Volunteerer'


@app.route("/about")
def about():
    return "about"


@app.route("/help")
def help():
    return "help"


@app.route("/edit/post/<postid>")
def edit_post(postid):
    return "edit post {}".format(postid)


@app.route("/edit/profile/<userid>")
def edit_profile(userid):
    return "edit profile {}".format(userid)


@app.route("/login")
def login():
    """
    email       (string)
    password    (string)
    """
    # we need to give the user a cookie, if they are not logged in, so that we can figure out if they are validated?
    return "login"


@app.route("/signup")
def signup():
    """
    email    (string)
    password (string) **not hashed yet!
    """
    return "signpup"


@app.route("/posts")
def posts():
    """
    we are going to have some filtering going on...
    """
    return "posts"


@app.route("/user_profile/<userid>")
def profile(userid):
    """
    userid (string)
    first_name (string)
    last_name (string)
    phone_number (number)
    email (string)
    """

    return userid


@app.route("/org_profile/<userid>")
def profile(userid):
    """
    userid (string)
    first_name (string)
    last_name (string)
    phone_number (number)
    email (string)
    """

    return userid


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='41001')
