#!/usr/bin/env python3
"""implement Basic Access Authentication Protocol
"""
from api.v1.auth.auth import Auth
from base64 import b64decode


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
        if (base64_authorization_header and isinstance(base64_authorization_header, str)):
            try:
                decode = b64decode(base64_authorization_header).decode("utf-8")
            except Exception:
                decode = None
        return decode
