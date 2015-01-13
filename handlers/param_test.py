__author__ = 'dog'

from base_image import BaseImageHandler

class ParamTest(BaseImageHandler):
    def get(self, *args, **kwargs):
        print type(self.check('name', 'name is ok.'))
        self.write("ok")