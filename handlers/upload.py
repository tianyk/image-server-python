#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import tornado.web
from PIL import Image
from bson import objectid

class UploadHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("upload.html")
    def post(self):
        files = self.request.files
        if files:
            for file in files['files']:
                splitext = os.path.splitext(file["filename"])
                filename = str(objectid.ObjectId()) + splitext[1]
                with open("upload/" + filename, "wb") as f:
                    f.write(file["body"])
                self.write({"filepath": filename})
        else:
            self.write('no file.')

