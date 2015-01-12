#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import datetime
import tornado.web
from PIL import ImageFile
from libs import MIME

IMAGE_INFO = "imageInfo"
IMAGE_VIEW = "imageView"
EXIF = "exif"
IMAGE_MOGR = "imageMogr"
WATER_MARK = "watermark"
IMAGE_AVE = "imageAve"

# @see https://infohost.nmt.edu/tcc/help/pubs/pil/formats.html
# http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html
IMAGE_FORMATS = {
    "jgp": "JPEG",
    "gif": "GIF",
    "png": "PNG",
    "webp": "WebP"
}


def merge_dict(source, target):
    # keys = [key for key in source]
    keys = list(source)[:]
    keys += [key for key in target if not key in keys]
    for key in keys:
        v1 = source.get(key, [])
        v2 = target.get(key, [])

        if not isinstance(v1, list):
            v1 = [v1]

        if isinstance(v2, list):
            v1 += v2
        else:
            v1.append(v2)

        source[key] = v1

    return source


def parse_qs(query):
    if not query:
        return

    encoded = {}
    args = query.split("/")
    interface = args[0]
    if IMAGE_INFO == interface:
        encoded["interface"] = IMAGE_INFO

    elif IMAGE_VIEW == interface:
        if len(args) <= 2:
            return
        encoded["interface"] = IMAGE_VIEW
        encoded["mode"] = args[1]
        # ["w", 2, "h", 2] ==> {"w": 2, "h": 2}
        params = dict(zip(*2 * (iter(args[2:]),)))
        merge_dict(encoded, params)

    elif EXIF == interface:
        encoded["interface"] = EXIF

    elif IMAGE_MOGR == interface:
        encoded["interface"] = IMAGE_MOGR

    elif WATER_MARK == interface:
        encoded["interface"] = WATER_MARK

    elif IMAGE_AVE == interface:
        encoded["interface"] = IMAGE_AVE

    else:
        return
    return encoded


class BaseImageHandler(tornado.web.RequestHandler):
    """docstring for BaseImageHandler"""

    def __init__(self, application, request, **kwargs):
        uri = request.uri
        params = parse_qs(request.query)
        if params:
            merge_dict(request.arguments, params)
            request.query_arguments = copy.deepcopy(request.arguments)

        super(BaseImageHandler, self).__init__(application, request, **kwargs)

    def write_image(self, im, file_name, ext, interlace='0'):
        output = StringIO()
        format = IMAGE_FORMATS.get(ext.lower(), "JPEG")

        if interlace == '1':
            try:
                im.save(output, "JPEG", quality=80, optimize=True, progressive=True)
            except IOError:
                ImageFile.MAXBLOCK = im.size[0] * im.size[1]
                im.save(output, "JPEG", quality=80, optimize=True, progressive=True)
        else:
            im.save(output, format, quality=80)
        img_data = output.getvalue()
        output.close()

        contentType = MIME.get(ext.lower(), "image/jpeg")
        self.set_header("Content-Type", contentType)
        expiry_time = datetime.datetime.utcnow() + datetime.timedelta(100)
        self.set_header("Expires", expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT"))
        # self.set_header("Cache-Control", "max-age=" + str(24 * 60 * 60))
        self.write(img_data)

    def write_blank(self):
        self.set_status(404)
        self.set_header("Content-Type", "text/plain")
        self.set_header("Cache-Control", "no-store")
        self.write("This request URL " + self.request.path + " was not found on this server.")