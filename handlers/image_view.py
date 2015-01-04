#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import tornado.web

IMAGE_INFO = "imageInfo"
IMAGE_VIEW = "imageView"
EXIF = "exif"
IMAGE_MOGR = "imageMogr"
WATER_MARK = "watermark"
IMAGE_AVE = "imageAve"


def _get_inteface(uri):
    print uri
    m = re.match(r".+\?(imageInfo|imageView|exif|imageMogr|watermark|imageAve)/.+", uri)

    if m:
        return m.group(1)
    else:
        return

class ImageViewHandler(tornado.web.RequestHandler):
    """
        添加一个写文件基础类，包含以下功能
        1.直接Write Image对象
        2.设置响应头，缓存文件
    """
    pass