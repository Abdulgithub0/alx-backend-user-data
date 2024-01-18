#!/usr/bin/env python3
"""implement Basic Access Authentication Protocol
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Subclass Auth template and define  BasicAuth protocol.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract a substring(base64 type) from a string.
        """
        _base64 = None
        if authorization_header and isinstance(authorization_header, str):
            if (authorization_header.startswith("Basic ")
               and not ("Basic  " in authorization_header)):
                _base64 = authorization_header[6:]
        return _base64

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ decode a base64 str
        """
        decode = None
        if (base64_authorization_header and
           isinstance(base64_authorization_header, str)):
            try:
                decode = b64decode(base64_authorization_header).decode("utf-8")
            except Exception:
                decode = None
        return decode

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """give user details from the decoded base64 string
        """
        detail = (None, None)
        if (decoded_base64_authorization_header and
           isinstance(decoded_base64_authorization_header, str)):
            if ":" in decoded_base64_authorization_header:
                detail = tuple(decoded_base64_authorization_header.split(":"))
        return detail

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """ returns the User instance based on email and password.
        """
        found_user = None
        match_users = None
        if user_email and user_pwd:
            if isinstance(user_email, str) and isinstance(user_pwd, str):
                try:
                    match_users = User.search({"email": user_email})
                except Exception:  # handle io error incase db contain no user
                    pass
                if match_users and len(match_users) > 0:
                    for user in match_users:
                        if user.is_valid_password(user_pwd):
                            found_user = user
        return found_user

    def current_user(self, request=None) -> TypeVar('User'):
        """ override the same method in Auth template and
            serve as frontend caller of other methods in this class
        """
        raw_auth = self.authorization_header(request)
        undecoded_b64 = self.extract_base64_authorization_header(raw_auth)
        decoded_b64 = self.decode_base64_authorization_header(undecoded_b64)
        credential = self.extract_user_credentials(decoded_b64)
        return self.user_object_from_credentials(*credential)
