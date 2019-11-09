import sys
import json

from flask import Flask, render_template, make_response, request
from backend.account import Person, Organization 
from backend.post import Post
from backend.token import TokenTable

sys.path.append('./frontend')
sys.path.append('./backend')

app = Flask(__name__)

@app.route("/")
def index():
    cookie = request.cookies.get("custom_token")
    return render_template("main.html", cookie=cookie)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/help")
def help():
    return render_template("help.html")


# TODO needs authentication
@app.route("/edit/post/<postid>")
def edit_post(postid):
    post = Post.init_from_uid(postid)
    # TODO edit the post object
    # TODO save the post object
    return "edit post {}".format(postid)


# TODO needs authentication
@app.route("/edit/profile/<userid>")
def edit_profile(userid):
    person = Person.init_from_uid(userid)
    # TODO edit the person object
    # TODO save the person object
    return "edit profile {}".format(userid)


@app.route("/login")
def login():
    """
    email       (string)
    password    (string)
    """
    # we need to give the user a cookie, if they are not logged in, so that we can figure out if they are validated?
    return get_handle_cookie(request, render_template("login.html"))
    # return 
    # return render_template("login.html")


@app.route("/signup")
def signup():
    """
    email    (string)
    password (string) **not hashed yet!
    """
    return "signpup"


# TODO if they are logged in, they can respond to the post
@app.route("/posts")
def posts():
    """
    we are going to have some filtering going on...
    """
    return "posts"


@app.route("/user_profile/<userid>")
def user_profile(userid):
    """
    userid (string)
    first_name (string)
    last_name (string)
    phone_number (number)
    email (string)
    """

    return userid


@app.route("/org_profile/<userid>")
def org_profile(userid):
    """
    userid (string)
    first_name (string)
    last_name (string)
    phone_number (number)
    email (string)
    """

    return userid


@app.route("/test", methods=["GET", "POST"])
def test():
    print(request.json)
    response = json.dumps({"status": "success"})
    return get_handle_cookie(request, response) # TODO think about the return type of handle_cookie - we are rendering
    # a template if we are NOT logged in, but what if it was a POST request or something??

    # name = request.cookies.get('userID')
    # if not name:
    #     resp = make_response(render_template('test.html'))
    #     resp.set_cookie('userID', "my_cookie")
    #     print(resp)
    #     print("NO COOKIES")
    #     return resp

    # return '<h1>welcome '+name+'</h1>'

# this should always be off a GET request
def get_handle_cookie(request, authed_response):
    cookie = request.cookies.get("custom_token")
    if not cookie:
        print("no cookie!")
        # if there was no cookie, we need to show them the login page
        # OR, if the cookie was invalidated or something?
        response = make_response(render_template("login.html"))
        response.set_cookie("custom_token", "TEST")
        return response

    return authed_response


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='41001')
