import json
import os
import pickle
from datetime import datetime, timedelta


def build_query_string(query_hash, user_id, end_cursor=None):
    """
    Formats a string with query_hash, user_id, end_cursor in their places
    Example:
        query_hash=query_hash.&variables={"id":"user_id","include_reel":true,"...}
    """
    hash = query_hash
    q_variables = {"id": user_id, "include_reel": "true","fetch_mutual": "false","first": 24}
    if end_cursor:
        q_variables['after'] = end_cursor
    return f"query_hash={hash}&variables={json.dumps(q_variables)}"


def handle_cookies(filename):
    """Checks for expiry date. Returns: cookies or None."""
    # check & validate cookies
    if not os.path.exists(filename):
        return None
    else:
        cookies = pickle.load(open('../' + filename, "rb"))
        for cookie in cookies:
            if 'expiry' in cookie.keys():
                expires = datetime.now() + timedelta(seconds=cookie['expiry'])
                if expires < datetime.now():
                    return None
        return cookies
