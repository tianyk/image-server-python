__author__ = 'dog'

from base_image import BaseImageHandler

class ParamTest(BaseImageHandler):
    def get(self, *args, **kwargs):
        self.check('name', 'name is ok.')["equals"]('ok')["equals"]("ok")
        self.write("ok")