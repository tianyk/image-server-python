#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import tornado.web

def resolve_argrments(uri):
    # m = re.match(r"(.+)?(.+)")
    pass


class BaseImageHandler(tornado.web.RequestHandler):
    """docstring for BaseImageHandler"""
    def __init__(self, application, request, **kwargs):
        uri = request.uri
        # 此处扩展原生的request对象，使用不同的参数解析规则
        # eg: /w/2/h/3
        # resolve_argrments
        request.query_arguments["test"] = request.arguments["test"] = "test"
        request.query_arguments["uri"] = request.arguments["uri"] = "uri"

        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
