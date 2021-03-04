class Users:
    prefix = "/user"
    user = prefix + "/"
    profile = prefix + "/me"


class Auth:
    prefix = "/auth"
    login = prefix + "/token"
    refresh_token = prefix + "/refresh_token"


class Books:
    prefix = "/book"
    create = prefix + "/create_book"