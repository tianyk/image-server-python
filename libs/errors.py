#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'tyk'


class DoogError(Exception):
    """Base class for all Doog exceptions.
    """


class InvalidRequestError(DoogError):
    def __init__(self, param, value, msg="Invalid value"):
        self.param = param
        self.msg = msg
        self.value = value


class ImageWaterMark(DoogError):
    def __init__(self, msg):
        self.msg = msg


class InvalidImageError(DoogError):
    def __init__(self, url):
        self.url = url
        self.msg = "This request URL " + url + " was not found on this server."


if __name__ == "__main__":
    error = InvalidImageError("www.baidu.com/logo.png")
    import json
    print json.dumps(error, default=lambda obj: obj.__dict__)