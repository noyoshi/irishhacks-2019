#
from flask import Blueprint,  request, redirect
from utils import get_userid, TOKEN_NAME, render_template, FAIL_MSG
from backend.post import Post
from backend.account import Account
import json


post_api = Blueprint('post_api', __name__)


@post_api.route("/grab_post", methods=["POST"])
def grab_post():
    user_id = get_userid()
    if not user_id:
        return FAIL_MSG

    user = Account.init_from_uuid(user_id)
    if not user:
        return FAIL_MSG

    post_id = request.json["post_id"]
    post = Post.init_from_uid(post_id)
    if not post.add_volunteer(user_id):
        return FAIL_MSG
    print("!!!!!!!!!!!!!!!!!!!!!!!!!")
    post.update_in_db()
    return json.dumps({"status": "success"})


@post_api.route("/posts/create/")
def create_post_view():
    user_id = get_userid()
    if not user_id:
        print("USER ID WAS BAD")
        return render_template("login.html")
    # token_conn = TokenTable()
    # user_id = token_conn.get_uuid(cookie)
    acc = Account.init_from_uuid(user_id)

    res = request.args
    print(res)
    print(request.form)
    if not res:
        return render_template("edit_post.html")
    res = dict(res)

    res['is_request'] = True
    res['length'] = res.get('duration')
    res['date'] = res.get('start_date')
    res['skill_set'] = res.get('skillset', [])

    post = acc.create_post(**res)
    # print("POSTS CREATE NEW")
    post = post.to_dict()
    # print(post)

    return redirect("/posts")


# TODO if they are logged in, they can respond to the post
@post_api.route("/posts")
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
        img_file = "meeting.jpg"
        if "tags" in post_dict and (post_dict["tags"] != None) and "technology" in post_dict["tags"]:
            img_file = "code.jpg"
        if "tags" in post_dict and (post_dict["tags"] != None) and "handy" in post_dict["tags"]:
            img_file = "handy.jpg"
        if "tags" in post_dict and (post_dict["tags"] != None) and "plumber" in post_dict["tags"]:
            img_file = "plumb.jpg"
        if user:
            post_dict["personal"] = 1 if user.is_personal else 2
            post_dict["img"] = img_file
            print(post_dict)
            print("found")
            tags = post_dict.get("tags", [])
            new_tags = []
            if tags:
                for t in tags:
                    new_tag = t.capitalize()
                    new_tags.append(new_tag)
                post_dict["tags"] = new_tags

            if post_dict["volunteers_required"] > 0:
                new_list.append(post_dict)
        else:
            print("not found", post_dict.items())

    return render_template("posts.html", posts=new_list)

# TODO if they are logged in, they can respond to the post
@post_api.route("/posts/add_to_post")
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

    return render_template("posts.html")


@post_api.route("/posts/<post_id>")
def view_post(post_id):
    """
    we are going to have some filtering going on...
    """

    # get post id from request, create post object, add a volunteer to the post object, update
    post = Post.init_from_uid(post_id)
    # Post.dump_table()
    if not post:
        print("bad post")
        return render_template("post.html")
    print("/posts/postid")
    post_d = post.to_dict()
    img_file = "meeting.jpg"
    user_id = post.user_id
    user_account = Account.init_from_uuid(user_id)
    if user_account and user_account.get_name():
        post_d["user_name"] = user_account.get_name()
    else:
        post_d["user_name"] = "No Name"

    if post.get_tags() and "technology" in post.get_tags():
        img_file = "code.jpg"
    if post.get_tags() and "handy" in post.get_tags():
        img_file = "handy.jpg"
    if post.get_tags() and "plumber" in post.get_tags():
        img_file = "plumb.jpg"
    return render_template("post.html", **post_d, img_file=img_file)


@post_api.route("/posts/create_new/", methods=["POST"])
def create_new_post():
    user_id = get_userid()
    if not user_id:
        print("USER ID WAS BAD")
        return json.dumps({"status": "failure"})

    # token_conn = TokenTable()
    # user_id = token_conn.get_uuid(cookie)
    acc = Account.init_from_uuid(user_id)

    res = request.json
    res = dict(res)
    print(res)

    res['is_request'] = True
    res['length'] = res.get('duration')
    res['date'] = res.get('start_date')
    res['skill_set'] = res.get('skillset', [])
    res['tags'] = res.get('tags', "").split(',')

    post = acc.create_post(**res)
    print("POSTS CREATE NEW!")
    post = post.to_dict()
    print(post)
    post['status'] = 'success'

    return json.dumps(post)
