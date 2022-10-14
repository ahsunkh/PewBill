import jwt
from rest_framework_simplejwt.tokens import RefreshToken

from pewbill.settings import SECRET_KEY


class PewBillJWT():

    def __init__(self):
        self.name = "pewbillJWT"

    def create_jwt(self, user):
        encoded_token = RefreshToken.for_user(user)
        access_token = str(encoded_token.access_token)
        return access_token, encoded_token

    def parse_token(self, token):
        token = token.split(" ")[1]
        return jwt.decode(token, SECRET_KEY, algorithms=["HS512"])['id'], token
