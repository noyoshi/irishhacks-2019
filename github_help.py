#
from github import Github
import os
from flask import Blueprint, render_template, request
from utils import get_userid

github_api = Blueprint('github_api', __name__)


github_username = os.getenv("github_bot_username")
github_password = os.getenv("github_bot_password")
# init github
g = Github(github_username, github_password)
repo = g.get_repo("noyoshi/irishhacks-2019")


@github_api.route("/help")
def help():
    # if they are logged in, they are going to have some small thing saying theya re looged in
    return render_template("help.html", token_uuid=get_userid())


@github_api.route("/post_help", methods=["POST"])
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
