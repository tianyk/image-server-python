#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import inspect
import urllib

from libs import errors, image_utils

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import datetime
import json
import tornado.web
from libs import MIME, validator, cache

IMAGE_INFO = "imageInfo"
IMAGE_VIEW = "imageView"
EXIF = "exif"
IMAGE_MOGR = "imageMogr"
WATER_MARK = "watermark"
IMAGE_AVE = "imageAve"


def item_index(arr, item):
    """
    获取元素在列表中的索引
    :param arr:
    :param item:
    :return:
    """
    for i, value in enumerate(arr):
        if value == item:
            return i
    return


def merge_dict(source, target):
    """
    合并两个字典。合并后的字典的value是一个列表。
    eg:
    doog_1 = {name: 'wangwang', age: 10}
    doog_2 = {name: 'wang~', gender: '♂'}
    合并以后
    doog = {name: ['wangwang', 'wang~'], age: 10, gender: '♂'}
    :param source:
    :param target:
    :return:
    """
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
        encoded["auto-orient"] = str("auto-orient" in args)
        encoded["strip"] = str("strip" in args)
        encoded["blur"] = str("blur" in args)

        args_name = ["thumbnail", "gravity", "crop", "rotate", "format", "interlace"]
        for arg_name in args_name:
            if arg_name in args:
                try:
                    encoded[arg_name] = args[item_index(args, arg_name) + 1]
                except IndexError:
                    pass
                except TypeError:
                    pass  # NoneType

    elif WATER_MARK == interface:
        if len(args) <= 2:
            return
        encoded["interface"] = WATER_MARK
        encoded["mode"] = args[1]
        params = dict(zip(*2 * (iter(args[2:]),)))
        merge_dict(encoded, params)
    elif IMAGE_AVE == interface:
        encoded["interface"] = IMAGE_AVE

    else:
        return
    return encoded


def check_param(self, getter):
    """
    参数校验
    :param getter:
    :return:
    """
    def check_handler(param, fail_msg="Invalid value"):
        value = getter(param)
        methods = {}

        def error_handler(msg):
            error = {"param": param, "msg": msg, "value": value}
            if not self._validationErrors:
                self._validationErrors = []
            self._validationErrors.append(error)

        def method_handler(method_name, *args):
            def invoke_method(*args):
                func = getattr(validator, method_name)
                if len(args) == 0:
                    is_correct = func(value)
                else:
                    is_correct = func(value, *args)

                if not is_correct:
                    error_handler(fail_msg)

                # 链式调用
                return methods

            return invoke_method

        for attr in dir(validator):
            if inspect.isfunction(getattr(validator, attr)):
                methods[attr] = method_handler(attr)

        return methods

    return check_handler


class BaseImageHandler(tornado.web.RequestHandler):
    """docstring for BaseImageHandler"""

    def __init__(self, application, request, **kwargs):
        super(BaseImageHandler, self).__init__(application, request, **kwargs)

        self.uri = request.uri
        self.query = request.query
        params = parse_qs(request.query)
        if params:
            merge_dict(request.arguments, params)
            request.query_arguments = copy.deepcopy(request.arguments)

        self._validationErrors = []

        def get_args(param):
            values = self.get_arguments(param, None)
            if not values:
                return
            if len(values) == 1:
                return values[0]
            else:
                return values

        self.check = check_param(self, get_args)

    _ARG_DEFAULT = []

    def get_arguments(self, name, strip=True, unquote=True):
        args = super(BaseImageHandler, self).get_arguments(name, strip=strip)
        if args and unquote:
            if isinstance(args, list):
                args = [urllib.unquote(x.encode('utf-8')) for x in args]
            elif isinstance(args, unicode):
                args = urllib.unquote(args.encode('utf-8'))

        return args

    def get_argument(self, name, default=_ARG_DEFAULT, strip=True, unquote=True):
        args = super(BaseImageHandler, self).get_argument(name, default=default, strip=strip)
        if args and unquote:
            if isinstance(args, list):
                args = [urllib.unquote(x) for x in args]
            elif isinstance(args, unicode):
                args = urllib.unquote(args.encode('utf-8'))

        return args

    def validation_errors(self, mapped=False):
        if len(self._validationErrors) == 0:
            return
        if mapped:
            errors = {}
            for err in self._validationErrors:
                errors[err["param"]] = err
            return errors
        return self._validationErrors

    @cache.cache_image
    def write_image(self, image_data, format):
        content_type = MIME.get(format.lower(), "image/jpeg")
        self.set_header("Content-Type", content_type)
        expiry_time = datetime.datetime.utcnow() + datetime.timedelta(100)
        self.set_header("Expires", expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT"))
        # self.set_header("Cache-Control", "max-age=" + str(10 * 365 * 24 * 60 * 60))
        self.write(image_data)

    def write_error(self, status_code, **kwargs):
        exc_info = kwargs.get("exc_info", None)
        if exc_info:
            error = exc_info[1]
            if isinstance(error, errors.DoogError):
                res = json.dumps(error, default=lambda obj: obj.__dict__)
                self.set_status(400)
                self.set_header("Content-Type", "application/json; charset=UTF-8")
                self.write(res)
                return
        if status_code == 400:
            super(BaseImageHandler, self).write_error(status_code, **kwargs)
        if status_code == 404:
            self.render('404.html')
        elif status_code == 500:
            self.render('500.html')
        else:
            # super(BaseImageHandler, self).write_error(status_code, **kwargs)
            self.render('500.html')