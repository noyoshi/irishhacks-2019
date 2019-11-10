
from flask import request
from backend.token import TokenTable
import json

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
