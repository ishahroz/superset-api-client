"""Custom Exception."""

import json

from requests import HTTPError


class NotFound(Exception):
    """Not found."""

    pass


class MultipleFound(Exception):
    """Multiple found."""

    pass


class QueryLimitReached(Exception):
    """Query limit reached."""

    pass


class BadRequestError(HTTPError):
    """Bad request error."""

    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop("message", None)
        super().__init__(*args, **kwargs)

    def __str__(self):
        return json.dumps(self.message, indent=4)


class ComplexBadRequestError(HTTPError):
    """Complex bad request error."""

    def __init__(self, *args, **kwargs):
        self.errors = kwargs.pop("errors", None)
        super().__init__(*args, **kwargs)

    def __str__(self):
        return json.dumps(self.errors, indent=4)
