from client.utils.helpers import build_query_string


class Profile:
    """
    Profile - represents an instagram user profile

    Attributes:
        session:    Requests session
        username:   An instagram username
        user_id:    An instagram user_id

    Methods:
        followers():    Returns a list of usernames that follows the user
        followings():   Returns a list of usernames that the user follows
    """

    __BASE_URL = "https://www.instagram.com"
    __DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"}
    __FOLLOWERS_QHASH = "5aefa9893005572d237da5068082d8d5"
    __FOLLOWINGS_QHASH = "3dec7e2c57367ef3da3d987d89f9dbc8"
    __QUERY_URL = __BASE_URL + "/graphql/query/?"

    def __init__(self, session, username, user_id):
        """Profile constructor."""
        self.__session = session
        self.__username = username
        self.__user_id = user_id

    def followers(self, end_cursor=None):
        """
        Returns response of the instagram api contains a list of first 24 followers.
        Use end cursor to get next list.
        """
        query_params = build_query_string(self.__FOLLOWERS_QHASH, self.__user_id, end_cursor)
        response = self.__session.get(self.__QUERY_URL + query_params, headers=self.__DEFAULT_HEADERS)
        if response.status_code == 200:
            return response.json()
        return None

    def followings(self, end_cursor=None):
        """
        Returns response of the instagram api contains a list of first 24 followings.
        Use end cursor to get next list.
        """
        query_params = build_query_string(self.__FOLLOWINGS_QHASH, self.__user_id, end_cursor)
        response = self.__session.get(self.__QUERY_URL + query_params, headers=self.__DEFAULT_HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
