#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web


class PhotoHandler(tornado.web.RequestHandler):
    def get(self, file_name, ext):
        self.write(self.request.uri + "  " + file_name + "  " + ext)