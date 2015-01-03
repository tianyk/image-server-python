#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        self.write('upload file.')

