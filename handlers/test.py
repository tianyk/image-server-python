#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(self.request.path + "\n")
        self.write(self.request.uri + "\n")
        self.write(self.request.query_arguments)
        # self.write(self.request.query_arguments + "\n")
        # for k, v in self.request.query_arguments:
        # self.write(k + ": " + v + "\n")

    def post(self):
        pass