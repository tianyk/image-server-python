__author__ = 'dog'

from base_image import BaseImageHandler


class ParamTest(BaseImageHandler):
    def get(self, *args, **kwargs):
        self.check('name', 'name is error.')["equals"]('ok')["equals"]("ok")
        errors = self.validation_errors(mapped=True)
        if errors:
            print errors
        self.write("ok")