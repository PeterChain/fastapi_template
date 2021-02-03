from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.models.users import User


class Token(object):
    """
    Token management
    """
    _access_token: str
    SECRET_KEY= "5d952bb23c4e495786787b8e21f2d656"
    ALGORITHM = "HS256"
    TOKEN_EXPIRE_MINUTES = 20

    @property
    def access_token(self):
        return self._access_token

    def __init__(self, token: str):
        super().__init__()
        self._access_token = token

    def create(user: User):
        expire = datetime.utcnow() + timedelta(Token.TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": user.username,
            "exp": expire
        }
        encoded_token = jwt.encode(to_encode, Token.SECRET_KEY, Token.ALGORITHM)
        return Token(encoded_token)

    def get_username(self):
        try:
            payload = jwt.decode(self._access_token, Token.SECRET_KEY, Token.ALGORITHM)
            username = payload.get("sub")
            if not username:
                return None
            return username
        except JWTError:
            return None
