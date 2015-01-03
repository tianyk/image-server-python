#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base_image_view import BaseImageHandler

class ImageViewTestHandler(BaseImageHandler):
    def get(self):
        uri = self.request.query_arguments.get("uri", None)
        test = self.request.query_arguments.get("test", None)

        uri_2 = self.request.arguments.get("uri", None)
        test_2 = self.request.arguments.get("test", None)


        resp = ""

        if uri:
            resp += uri
        if test:
            resp += test
        if uri_2:
            resp += uri_2
        if test_2:
            resp += test_2

        self.write(resp)
