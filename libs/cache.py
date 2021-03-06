#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'tyk'

import base64
import functools
import memcache
import image_utils


mc = memcache.Client(['10.101.110.17:11211'])


def load_image(func):
    """
    GET图片时先从缓存中拿，拿不到再处理。
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kw):
        that = args[0]
        ext = args[2]
        uri = that.uri
        key = base64.urlsafe_b64encode(uri)
        try:
            image_data = mc.get(key)
            format = mc.get("format_" + key) or ext
            if image_data:
                that.write_image(image_data, format)
                return
        except:
            pass

        return func(*args, **kw)

    return wrapper


def cache_image(func):
    """
    写图片时，缓存图片
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kw):
        that = args[0]
        uri = that.uri
        key = base64.urlsafe_b64encode(uri)
        image_data = args[1]
        format = args[2]
        try:
            # 避免重复缓存。待优化
            if not mc.get(key):
                # 真实格式
                mc.set("format_" + key, format)
                mc.set(key, image_data)
        except:
            pass

        return func(*args, **kw)

    return wrapper
