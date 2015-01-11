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
    size = im.size
    origin_long_edge = max(size)
    origin_short_edge = min(size)

    ratio_long = ratio_short = 1 # 默认值取1，后期取min值，如果min值大于1直接返回。如果不返回，必有一个小于1。
    if long_edge:
        long_edge = int(long_edge)
        ratio_long = long_edge / origin_long_edge
    if short_edge:
        short_edge = int(short_edge)
        ratio_short = short_edge / origin_short_edge

    min_ratio = min(ratio_long, ratio_short)
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

    size = im.size
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

    if min_ratio >= 1: # 两边大
        return

    if max_ratio < 1: # 两者均小于原来
        size = resize = tuple(int(x * max_ratio) for x in size)
        im = im.resize(resize)
    box = []
    box.append(int((size[0] - w) / 2))
    box.append(int((size[1] - h) / 2))
    box.append(w + box[0])
    box.append(h + box[1])

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

    size = im.size
    ratio_w = ratio_h = 1
    if w:
        w = int(w)
        ratio_w = w / size[0]
    if h:
        h = int(h)
        ratio_h = h / size[1]

    min_ratio = min(ratio_w, ratio_h)
    if min_ratio >= 1:
        return

    resize = tuple(int(x * min_ratio) for x in size)
    im = im.resize(resize)
    return im

def image_view_mode_3(im, w, h):
    """
    限定缩略图的宽最少为<Width>，高最少为<Height>，进行等比缩放，不裁剪。
    """
    if not w and not h:
        return

    size = im.size
    if not w:
        h = int(h)
        w = h
    if not h:
        w = int(w)
        h = w

    ratio_w = w / size[0]
    ratio_h = h / size[1]
    max_ratio = max(ratio_w, ratio_h)
    if max_ratio >= 1:
        return

    resize = tuple(int(x * max_ratio) for x in size)
    im = im.resize(resize)
    return im

def image_view_mode_4(im, long_edge, short_edge):
    """
    限定缩略图的长边最少为<LongEdge>，短边最少为<ShortEdge>，进行等比缩放，不裁剪。
    这个模式很适合在手持设备做图片的全屏查看（把这里的长边短边分别设为手机屏幕的分辨率即可），
    生成的图片尺寸刚好充满整个屏幕（某一个边可能会超出屏幕）。
    """
    if not long_edge and not short_edge:
        return
    size = im.size
    origin_long_edge = max(size)
    origin_short_edge = min(size)

    if not long_edge:
        short_edge = int(short_edge)
        long_edge = short_edge
    if not short_edge:
        long_edge = int(long_edge)
        short_edge = long_edge

    ratio_long = long_edge / origin_long_edge
    ratio_short = short_edge / origin_short_edge

    max_ratio = max(ratio_long, ratio_short)
    if max_ratio >= 1:
        return

    resize = tuple(int(x * max_ratio) for x in size)
    im = im.resize(resize)
    return im

def image_view_mode_5(im, long_edge, short_edge):
    """
    限定缩略图的长边最少为<LongEdge>，短边最少为<ShortEdge>，进行等比缩放，居中裁剪。
    同上模式4，但超出限定的矩形部分会被裁剪。
    """
    if not long_edge and not short_edge:
        return

    size = im.size
    origin_long_edge = max(size)
    origin_short_edge = min(size)

    if not long_edge:
        short_edge = int(short_edge)
        long_edge = short_edge
    if not short_edge:
        long_edge = int(long_edge)
        short_edge = long_edge

    long_edge = min(int(long_edge), origin_long_edge)
    short_edge = min(int(short_edge), origin_short_edge)

    ratio_long = long_edge / origin_long_edge
    ratio_short = short_edge / origin_short_edge
    min_ratio = min(ratio_long, ratio_short)
    max_ratio = max(ratio_long, ratio_short)

    if min_ratio >= 1:
        return

    box = []
    if max_ratio < 1:
        size = resize = tuple(int(x * max_ratio) for x in size)
        im = im.resize(resize)

    if size[0] >= size[1]: # 横向
        box.append(int((size[0] - long_edge) / 2))
        box.append(int((size[1] - short_edge) / 2))
        box.append(box[0] + long_edge)
        box.append(box[1] + short_edge)
    else: # 竖向
        box.append(int((size[0] - short_edge) / 2))
        box.append(int((size[1] - long_edge) / 2))
        box.append(box[0] + short_edge)
        box.append(box[1] + long_edge)

    im = im.crop(tuple(box))
    return im