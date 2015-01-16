#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

from PIL import Image, ExifTags

from base_image import BaseImageHandler
from libs import image_utils, upload


IMAGE_INFO = "imageInfo"
IMAGE_VIEW = "imageView"
EXIF = "exif"
IMAGE_MOGR = "imageMogr"
WATER_MARK = "watermark"
IMAGE_AVE = "imageAve"

UPLOAD_DIR = 'upload/'


class ImageViewHandler(BaseImageHandler):
    def get(self, filename, ext):
        filepath = upload.get_file_path(filename, ext)
        if not filepath:
            self.write_blank()
            return

        try:
            im = Image.open(filepath)
        except IOError:
            self.write_blank()
            return

        # 接口标识
        interface = self.get_argument("interface", None)
        if not interface:  # 直接返回原图
            self.write_image(im, filename, ext)

        elif IMAGE_INFO == interface:  # 图片基本信息
            size = im.size
            info = {}
            info["format"] = im.format or 'None'
            info["width"] = size[0]
            info["height"] = size[1]
            info["colorModel"] = im.mode
            self.write(info)

        elif IMAGE_VIEW == interface:  # 图片处理
            self.check("w")["is_positive_int"]()
            self.check("h")["is_positive_int"]()
            self.check("format", "Unsupported format")["is_in"](["jpg", "jpeg", "gif", "png"])
            self.check("interlace")["is_in"](["0", "1"])

            errors = self.validation_errors()
            if errors:
                self.write_json(errors)
                return

            mode = self.get_argument("mode", None)
            w = self.get_argument("w", None)
            h = self.get_argument("h", None)
            format = self.get_argument("format", None)
            interlace = self.get_argument("interlace", None)

            size = im.size
            if "0" == mode:
                re_im = image_utils.image_view_mode_0(im, w, h)
                if re_im:
                    im = re_im
            elif "1" == mode:
                re_im = image_utils.image_view_mode_1(im, w, h)
                if re_im:
                    im = re_im
            elif "2" == mode:
                re_im = image_utils.image_view_mode_2(im, w, h)
                if re_im:
                    im = re_im
            elif "3" == mode:
                re_im = image_utils.image_view_mode_3(im, w, h)
                if re_im:
                    im = re_im
            elif "4" == mode:
                re_im = image_utils.image_view_mode_4(im, w, h)
                if re_im:
                    im = re_im
            elif "5" == mode:
                re_im = image_utils.image_view_mode_5(im, w, h)
                if re_im:
                    im = re_im
            else:
                pass

            if format:  # 首先校验format是否被支持
                ext = format

            if interlace:
                self.write_image(im, filename, ext, interlace)
            else:
                self.write_image(im, filename, ext)

        elif EXIF == interface:
            exif = im._getexif()
            if exif:
                # dict(zip(d.keys(), map(lambda x:x * 2, d.values())))
                # dict((k, v*2) for k, v in {'a': 1, 'b': 2}.items())
                exif = dict((ExifTags.TAGS.get(k, k), v) for k, v in exif.items())
                self.write(exif)
            else:
                self.write({"errcode": 400, "errmsg": "no exif info"})
            return
        elif IMAGE_MOGR == interface:
            pass
        elif WATER_MARK == interface:
            pass
        elif IMAGE_AVE == interface:
            pass
        else:  # 直接返回原图
            self.write_image(im, filename, ext)