#!/usr/bin/env python3
"""implement Basic Access Authentication Protocol
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Subclass Auth template and define  BasicAuth protocol.
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract a substring(base64 type) from a string.
        """
        _base64 = None
        if authorization_header and type(authorization_header) is str:
            if (authorization_header.startswith("Basic ")
               and not ("Basic  " in authorization_header)):
                _base64 = authorization_header.split()
                _base64 = _base64[1] if len(_base64) == 2 else None
        return _base64
