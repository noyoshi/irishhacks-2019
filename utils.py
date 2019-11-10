
from flask import request, render_template
from backend.token import TokenTable
import json


def wrapper(func):
    def f(*args, **kwargs):
        kwargs["token_uuid"] = get_userid()
        return func(*args, **kwargs)
    return f


render_template = wrapper(render_template)

TOKEN_NAME = "custom_token"
FAIL_MSG = json.dumps({"status": "failure"})


def get_userid():
    token_conn = TokenTable()
    cookie = request.cookies.get("custom_token")
    print(cookie)
    user_id = token_conn.get_uuid(cookie)
    if not user_id or not token_conn.validate(user_id, cookie):
        print("INVALID_TOKEN: {}".format(cookie))
        return None

    return user_id
