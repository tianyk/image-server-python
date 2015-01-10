#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

def image_view_mode_0(im, long_edge, short_edge):
    """
        限定缩略图的长边最多为<LongEdge>，短边最多为<ShortEdge>，进行等比缩放，不裁剪。
        如果只指定 w 参数则表示限定长边（短边自适应），只指定 h 参数则表示限定短边（长边自适应）。
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
        return
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
        return
    resize = tuple(int(x * min_ratio) for x in size)

    im = im.resize(resize)
    return im

def image_view_mode_1(im, w, h):
    """
    限定缩略图的宽最少为<Width>，高最少为<Height>，进行等比缩放，居中裁剪。
    转后的缩略图通常恰好是 <Width>x<Height> 的大小（有一个边缩放的时候会因为超出矩形框而被裁剪掉多余部分）。
    如果只指定 w 参数或只指定 h 参数，代表限定为长宽相等的正方图。
    """
    if not w and not h:
        return

    # size = im.size()
    # if not w: # 宽度不存在
    #     h = min(int(h), size[1]) # 高度最大为原始高度
    #     w = min(h, size[0]) # 宽度不存在等于高度，宽度最大为原始宽度
    # if not h:
    #     w = min(int(w), size[0]) # 宽度最大为原始宽度
    #     h = min(w, size[1]) # 高度不存在等于宽度，高度最大为原始高度

    # w = int(w)
    # h = int(h)
    # if w >= size[0] and h >= size[1]:
    #     return

    size = im.size()
    if not w:
        h = int(h)
        w = min(h, size[0])
    if not h:
        w = int(w)
        h = min(w, size[1])

    w = int(w)
    h = int(h)

    ratio_w = w / size[0]
    ratio_h = h / size[1]
    max_ratio = max(ratio_w, ratio_h)
    min_ratio = min(ratio_w, ratio_h)

    box = []
    if min_ratio >= 1: # 两边大
        return
    elif max_ratio >= 1: # 一边大
        box[0] = int((size[0] - w) / 2)
        box[1] = int((size[1] - h) / 2)
        box[2] = w + box[0]
        box[3] = h + box[1]
    else: # 二者均小于1
        resize = tuple(int(x * max_ratio) for x in size)
        im = im.resize(resize)
        box[0] =

    im = im.crop(tuple(box))
    return im

def image_view_mode_2(im, w, h):
    """
    限定缩略图的宽最多为<Width>，高最多为<Height>，进行等比缩放，不裁剪。
    如果只指定 w 参数则表示限定宽度（高度自适应），只指定 h 参数则表示限定高度（宽度自适应）。
    它和模式0类似，区别只是限定宽和高，不是限定长边和短边。
    从应用场景来说，模式0适合移动设备上做缩略图，模式2适合PC上做缩略图。
    eg:

    """
    if not w and not h:
        return

    size = im.size()
    ratio_w = ratio_h = -1
    if w:
        w = int(w)
        ratio_w = w / size[0]
    if h:
        h = int(h)
        ratio_h = h / size[1]

    if ratio_w == -1:
        ratio_w = ratio_h
    if ratio_h == -1:
        ratio_h = ratio_w

    min_ratio = min(ratio_w, ratio_h)
    if min_ratio >= 1:
        return
    resize = tuple(int(x * min_ratio) for x in size)
    im = im.resize(resize)
    return im

def iamge_view_mode_3(im, w, h):
    """
    限定缩略图的宽最少为<Width>，高最少为<Height>，进行等比缩放，不裁剪。
    """
    if not w and not h:
        return

    size = im.size()
    ratio_w = ratio_h = -1
    if w:
        w = int(w)
        ratio_w = w / size[0]
    if h:
        h = int(h)
        ratio_h = h / size[1]

    if ratio_w == -1:
        ratio_w = ratio_h
    if ratio_h == -1:
        ratio_h = ratio_w

    max_ratio = max(ratio_w, ratio_h)
    if max_ratio >= 1:
        return

    resize = tuple(int(x * min_ratio) for x in size)
    im = im.resize(resize)
    return im

def image_view_mode_4(im, long_edge, short_edge):
    """
    限定缩略图的长边最少为<LongEdge>，短边最少为<ShortEdge>，进行等比缩放，不裁剪。
    这个模式很适合在手持设备做图片的全屏查看（把这里的长边短边分别设为手机屏幕的分辨率即可），
    生成的图片尺寸刚好充满整个屏幕（某一个边可能会超出屏幕）。
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