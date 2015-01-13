#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from libs import upload


UPLOAD_DIR = 'upload/'


class UploadHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("upload.html")

    def post(self):
        files = self.request.files
        persistentOps = self.get_body_argument("persistentOps", None)
        if files:
            for file in files['files']:
                content_type = file["content_type"]
                if content_type.startswith("image/"):
                    filepath = upload.generate_filepath(file["filename"])
                    with open("/".join(filepath), "wb") as f:
                        f.write(file["body"])

                    self.write({"filepath": filepath[1]})
                else:
                    self.write('not image file.')
            if persistentOps:
                print persistentOps
        else:
            self.write('no file.')

