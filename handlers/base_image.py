#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import copy
import re
import tornado.web

IMAGE_INFO = "imageInfo"
IMAGE_VIEW = "imageView"
EXIF       = "exif"
IMAGE_MOGR = "imageMogr"
WATER_MARK = "watermark"
IMAGE_AVE  = "imageAve"


def merge_dict(source, target):
    keys = [key for key in source]
    keys += [key for key in target if not key in keys]
    for key in keys:
        v1 = source.get(key, [])
        v2 = target.get(key, [])

        if not isinstance(v1, list):
            v1 = [v1]

        if isinstance(v2, list):
            v1 = v1 + v2
        else:
            v1.append(v2)

        source[key] = v1

    return source

def parse_qs(query):
    if not query:
        return

    encoded = {}
    args = query.split("/")
    interface = args[0]
    if IMAGE_INFO   == interface:
        encoded["interface"] = IMAGE_INFO
    elif IMAGE_VIEW == interface:
        if len(args) <= 2:
            return
        encoded["interface"] = IMAGE_VIEW
        encoded["mode"] = args[1]
        # ["w", 2, "h", 2] ==> {"w": 2, "h": 2}
        params = dict(zip(*2 * (iter(args[2:]),)))
        merge_dict(encoded, params)

    elif EXIF       == interface:
        encoded["interface"] = EXIF
    elif IMAGE_MOGR == interface:
        encoded["interface"] = IMAGE_MOGR
    elif WATER_MARK == interface:
        encoded["interface"] = WATER_MARK
    elif IMAGE_AVE  == interface:
        encoded["interface"] = IMAGE_AVE
    else:
        return
    return encoded


class BaseImageHandler(tornado.web.RequestHandler):
    """docstring for BaseImageHandler"""
    def __init__(self, application, request, **kwargs):
        uri = request.uri
        # 此处扩展原生的request对象，使用不同的参数解析规则
        # eg: /w/2/h/3
        # parse_qs
        params = parse_qs(request.query)
        if params:
            merge_dict(request.arguments, params)
            request.query_arguments = copy.deepcopy(request.arguments)
        super(BaseImageHandler, self).__init__(application, request, **kwargs)

# source = {"w" : 1, "h": 2}
# target = {"r": 3}
# merge_dict(source, target)
# print source
# dict3 = {"w": 3, "r": [4, 5]}
# print merge_dict(source, dict3)