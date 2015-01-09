#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

def image_view_mode_0(im, long_edge, short_edge):
    """
        长边最多为long_edge，短边最多为short_edge
        eg:
                w = 1000
                h = 600
                origin_long_edge = 1000
                origin_short_edge = 600

                long_edge = 800
                short_edge = 600

                ratio_long = 800 / 1000 = 0.8
                ratio_short = 600 / 600 = 1
                # 取比例的最小值
                min_ratio = 0.8

                resize_long_edge = 1000 * 0.8 = 800 # 长边最多800
                resize_short_edge = 600 * 0.8 = 480 # 短边最多600
    """
    if not long_edge and not short_edge:
        return im
    size = im.size()
    origin_long_edge = max(size)
    origin_short_edge = min(size)

    ratio_long = ratio_short = -1
    if long_edge:
        long_edge = int(long_edge)
        ratio_long = long_edge / origin_long_edge
    if short_edge:
        short_edge = int(short_edge)
        ratio_short = short_edge / origin_short_edge

    if -1 == ratio_long:
        ratio_long = ratio_short
    elif -1 == ratio_short:
        ratio_short = ratio_long

    min_ratio = min(ratio_long, ratio_short)
    # 新图的宽/高/长边/短边，不会比原图大，即本接口总是缩小图片；
    if min_ratio >= 1:
        return im
    resize = tuple(int(x * min_ratio) for x in size)

    im = im.resize(resize)
    return im

def image_view_mode_1(im, w, h):
    if not w and not h: # 暂时返回原图，后期改为参数错误
        return im
    if not w:
        w = h
    if not h:
        h = w
    w = int(w)
    h = int(h)

    ratio_w = ratio_h = -1
    if w:
        ratio_w = w / size[0]
    if h:
        ratio_h = h / size[1]
    max_ratio = max(ratio_w, ratio_h)
    if max_ratio >= 1:
        return im

    resize = []
    box = [0, size[0], size[1], 0]
    if 1 != ratio: # > 1 resize
        if ratio_w > ratio_h:
            resize = tuple(int(x * ratio_w) for x in size)
            box[0] = 0
            box[2] = w
            box[1] = int(h * (ratio_w - 1) / 2)
            box[3] = h + box[1]
        else:
            resize = tuple(int(x * ratio_h) for x in size)
            box[1] = 0
            box[3] = h
            box[0] = int(w * (ratio_h - 1) / 2)
            box[2] = w + box[0]

        resize = tuple(resize)
        im = im.resize(resize)
    else: # ratio <= 1 no resize
        box[0] = int((size[0] - w) / 2)
        box[2] = w + box[0]
        box[1] = int((size[1] - h) / 2)
        box[3] = h + box[1]

    im = im.crop(tuple(box))

def image_view_mode_4(im, long_edge, short_edge):
    """
        长边最少为long_edge，短边最少为short_edge
        eg:
                w = 1000
                h = 600
                origin_long_edge = 1000
                origin_short_edge = 600

                long_edge = 800
                short_edge = 800

                ratio_long = 800 / 1000 = 0.8
                ratio_short = 800 / 600 = 1.34
                # 取比例的最小值
                max_ratio = 1

                resize_long_edge = 1000 * 1.34 = 1340 # 长边最少800
                resize_short_edge = 600 * 1.34 = 800 # 短边最少800
    """
    if not long_edge and not short_edge:
        return im
    size = im.size()
    origin_long_edge = max(size)
    origin_short_edge = min(size)

    ratio_long = ratio_short = -1
    if long_edge:
        long_edge = int(long_edge)
        ratio_long = long_edge / origin_long_edge
    if short_edge:
        short_edge = int(short_edge)
        ratio_short = short_edge / origin_short_edge

    if -1 == ratio_long:
        ratio_long = ratio_short
    elif -1 == ratio_short:
        ratio_short = ratio_long

    max_ratio = max(ratio_long, ratio_short)
    # 新图的宽/高/长边/短边，不会比原图大，即本接口总是缩小图片；
    if max_ratio >= 1:
        return im
    resize = tuple(int(x * max_ratio) for x in size)

    im = im.resize(resize)
    return im