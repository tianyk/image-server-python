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


class FileNotFoundError(DoogError):
    def __init__(self, url):
        self.url = url
        self.msg = "File Not Fount."


class InvalidImageError(DoogError):
    def __init__(self, filename, msg="invalid image File."):
        self.filename = filename
        self.msg = msg


class ImageExifError(DoogError):
    def __init__(self, filename, msg="no exif info."):
        self.filename = filename
        self.msg = msg


class FontNotSupport(DoogError):
    def __init__(self, font, msg="unsupported font."):
        self.font = font
        self.msg = msg


if __name__ == "__main__":
    error = FileNotFoundError("www.baidu.com/logo.png")
    import json
    print json.dumps(error, default=lambda obj: obj.__dict__)