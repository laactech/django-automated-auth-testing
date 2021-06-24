from enum import Enum, unique
from typing import Tuple


@unique
class HttpMethod(Enum):
    GET = "GET"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"

    @classmethod
    def safe_methods(cls) -> Tuple["HttpMethod", "HttpMethod", "HttpMethod"]:
        return cls.GET, cls.HEAD, cls.OPTIONS

    @classmethod
    def unsafe_methods(cls) -> Tuple["HttpMethod", "HttpMethod", "HttpMethod", "HttpMethod"]:
        return cls.POST, cls.PATCH, cls.PUT, cls.DELETE

    @classmethod
    def all_methods(cls) -> tuple:
        return tuple(cls)
