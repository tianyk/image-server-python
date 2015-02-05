#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import urllib
import base64
from PIL import Image, ExifTags
from base_image import BaseImageHandler
from libs import image_utils, upload, download, fonts
from libs.errors import InvalidRequestError, ImageWaterMark, FileNotFoundError, InvalidImageError

TEMP_DIR = "temp/"
IMAGE_INFO = "imageInfo"
IMAGE_VIEW = "imageView"
EXIF = "exif"
IMAGE_MOGR = "imageMogr"
WATER_MARK = "watermark"
IMAGE_AVE = "imageAve"


class ImageViewHandler(BaseImageHandler):
    def get(self, filename, ext):
        file_path = upload.get_file_path(filename, ext)
        if not file_path:
            raise FileNotFoundError(filename + "." + ext)

        try:
            im = Image.open(file_path)
        except IOError:
            raise InvalidImageError(filename + "." + ext)

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
                self.write_check_errors(errors)
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

            if format:  # 首先校验format是否被支持
                ext = format

            if interlace:
                self.write_image(im, filename, ext, interlace=interlace)
            else:
                self.write_image(im, filename, ext)

        elif EXIF == interface:
            exif = im._getexif()
            if exif:
                # dict(zip(d.keys(), map(lambda x:x * 2, d.values())))
                # dict((k, v*2) for k, v in {'a': 1, 'b': 2}.items())
                exif = dict((ExifTags.TAGS.get(k, k), v) for k, v in exif.items() if k in ExifTags.TAGS)
                self.write_check_errors(exif)
            else:
                # self.write({"errcode": 400, "errmsg": "no exif info"})
                raise FileNotFoundError(filename + "." + ext)

        elif IMAGE_MOGR == interface:
            self.check("NorthWest")["is_in"](["NorthWest", "North", "NorthEast",
                                              "West", "Center", "East", "SouthWest", "South", "SouthEast"])

            args = self.query.split("/")
            # 保证顺序
            for arg in args:
                if "auto-orient" == arg:
                    auto_orient = self.get_argument("auto-orient", None)
                    if "True" == auto_orient:
                        im = image_utils.image_mogr_auto_orient(im)
                elif "strip" == arg:
                    strip = self.get_argument("strip", None)
                    if "True" == strip:
                        im = image_utils.image_mogr_strip(im)
                elif "thumbnail" == arg:
                    thumbnail = self.get_argument("thumbnail", None)
                    if thumbnail:
                        im = image_utils.image_mogr_thumbnail(im, urllib.unquote(thumbnail))
                elif "crop" == arg:
                    gravity = self.get_argument("gravity", "NorthWest")
                    crop = self.get_argument("crop", None)
                    if crop:
                        im = image_utils.image_mogr_crop(im, gravity, crop)
                elif "rotate" == arg:
                    rotate = self.get_argument("rotate", None)
                    if rotate:
                        im = image_utils.image_mogr_rotate(im, rotate)
                elif "blur" == arg:
                    blur = self.get_argument("blur", None)
                    if "True" == blur:
                        im = image_utils.image_mogr_blur(im)

            format = self.get_argument("format", None)
            interlace = self.get_argument("interlace", None)
            if format:  # 首先校验format是否被支持
                ext = format

            if interlace:
                self.write_image(im, filename, ext, interlace)
            else:
                self.write_image(im, filename, ext)

        elif WATER_MARK == interface:
            mode = self.get_argument("mode", None)

            size = im.size
            if "1" == mode:
                self.check("image")["not_empty"]()["is_base64"]()
                self.check("dx")["is_positive_int"]()
                self.check("dy")["is_positive_int"]()

                errors = self.validation_errors()
                if errors:
                    self.write_check_errors(errors)
                    return

                # 图片水印
                image = self.get_argument("image", None)
                dissolve = self.get_argument("dissolve", "100")
                gravity = self.get_argument("gravity", "SouthEast")
                dx = self.get_argument("dx", "10")
                dy = self.get_argument("dy", "10")

                image = base64.urlsafe_b64decode(image)
                # 有URL暂时改为文件名
                # image_name = download.download_image(image)
                mark_filename, mark_ext = os.path.splitext(image)
                mark_im_path = upload.get_file_path(mark_filename, mark_ext[1:])
                if not mark_im_path:
                    raise FileNotFoundError(mark_filename + mark_ext)
                else:
                    mark_im = Image.open(mark_im_path)
                    im = image_utils.image_water_mark_image(im, mark_im, dissolve=dissolve,
                                                            gravity=gravity, dx=int(dx), dy=int(dy))

            elif "2" == mode:
                self.check("text")["not_empty"]()["is_base64"]()
                self.check("font")["is_in"](fonts.fonts.keys())["is_base64"]()
                self.check("format", "Unsupported format")["is_in"](["jpg", "jpeg", "gif", "png"])
                self.check("fill")["is_base64"]()
                self.check("interlace")["is_in"](["0", "1"])
                self.check("dx")["is_positive_int"]()
                self.check("dy")["is_positive_int"]()

                errors = self.validation_errors()
                if errors:
                    self.write_check_errors(errors)
                    return

                # 文字水印
                text = self.get_argument("text", None)
                font = self.get_argument("font", base64.urlsafe_b64encode("黑体"))
                fontsize = self.get_argument("fontsize", "0")
                fill = self.get_argument("fill", base64.urlsafe_b64encode("white"))
                dissolve = self.get_argument("dissolve", "100")
                gravity = self.get_argument("gravity", "SouthEast")
                dx = self.get_argument("dx", "10")
                dy = self.get_argument("dy", "10")

                # http://stackoverflow.com/questions/2941995/python-ignore-incorrect-padding-error-when-base64-decoding
                text = base64.urlsafe_b64decode(text)
                font = base64.urlsafe_b64decode(font)
                fill = base64.urlsafe_b64decode(fill)

                im = image_utils.image_water_mark_text(im, text, font=font, fontsize=int(fontsize), fill=fill,
                                                       dissolve=dissolve, gravity=gravity, dx=int(dx), dy=int(dy))

            format = self.get_argument("format", None)
            interlace = self.get_argument("interlace", None)
            if format:  # 首先校验format是否被支持
                ext = format

            if interlace:
                self.write_image(im, filename, ext, interlace)
            else:
                self.write_image(im, filename, ext)
        elif IMAGE_AVE == interface:
            im_ave = image_utils.image_ave(im)
            self.write_check_errors({im.mode: im_ave})
        else:  # 直接返回原图
            self.write_image(im, filename, ext)