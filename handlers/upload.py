#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web

from libs import upload
from base_image import BaseImageHandler

UPLOAD_DIR = 'upload/'


class UploadHandler(BaseImageHandler):
    def get(self, *args, **kwargs):
        self.render("upload.html")

    def post(self):
        files = self.request.files.get("files", None)
        # 预处理参数
        # persistentOps = self.get_body_argument("persistentOps", None)
        if files and len(files) > 0:
            # 现阶段只支持一个文件上传
            file = files[-1]
            content_type = file["content_type"]
            if content_type.startswith("image/"):
                file_path = upload.generate_file_path(file["filename"])
                with open("/".join(file_path), "wb") as f:
                    f.write(file["body"])

                self.write_check_errors({"file_path": file_path[1]})
            else:
                self.write('Unsupported format')

                # for file in files['files']:
                # content_type = file["content_type"]
                # if content_type.startswith("image/"):
                #         file_path = upload.generate_file_path(file["filename"])
                #         with open("/".join(file_path), "wb") as f:
                #             f.write(file["body"])
                #
                #         self.write_json({"file_path": file_path[1]})
                #     else:
                #         self.write('Unsupported format')
                # if persistentOps:
                #     pass
        else:
            self.write('no file.')

