#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import tornado.web

IMAGE_INFO = "imageInfo"
IMAGE_VIEW = "imageView"
EXIF       = "exif"
IMAGE_MOGR = "imageMogr"
WATER_MARK = "watermark"
IMAGE_AVE  = "imageAve"

from base_image import BaseImageHandler

class ImageViewHandler(BaseImageHandler):
    def get(self):
        interface = self.get_argument("interface", None)
        if not interface:
            # 直接返回图片
            pass
        elif IMAGE_INFO == interface:
            pass
        elif IMAGE_VIEW == interface:
            pass
        elif EXIF       == interface:
            pass
        elif IMAGE_MOGR == interface:
            pass
        elif WATER_MARK == interface:
            pass
        elif IMAGE_AVE  == interface:
            pass
        else:
            # 直接返回原图
            pass