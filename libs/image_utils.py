#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import re
from PIL import Image, ImageFilter, ImageColor, ImageFont, ImageDraw
from libs import fonts


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

    ratio_long = ratio_short = 1  # 默认值取1，后期取min值，如果min值大于1直接返回。如果不返回，必有一个小于1。
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

    if min_ratio >= 1:  # 两边大
        return

    if max_ratio < 1:  # 两者均小于原来
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

    if size[0] >= size[1]:  # 横向
        box.append(int((size[0] - long_edge) / 2))
        box.append(int((size[1] - short_edge) / 2))
        box.append(box[0] + long_edge)
        box.append(box[1] + short_edge)
    else:  # 竖向
        box.append(int((size[0] - short_edge) / 2))
        box.append(int((size[1] - long_edge) / 2))
        box.append(box[0] + short_edge)
        box.append(box[1] + long_edge)

    im = im.crop(tuple(box))
    return im


def image_mogr_auto_orient(im):
    """
    根据原图EXIF信息自动旋正，便于后续处理建议放在首位。

      1        2       3      4         5            6           7          8

    888888  888888      88  88      8888888888  88                  88  8888888888
    88          88      88  88      88  88      88  88          88  88      88  88
    8888      8888    8888  8888    88          8888888888  8888888888          88
    88          88      88  88
    88          88  888888  888888

    :rtype : Image
    :param im:
    """
    exif = im._getexif()
    if exif and exif.get(0x0112, None):
        orientation = exif.get(0x0112, None)
        if orientation == 1:
            pass
        elif orientation == 2:
            im.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            im.transpose(Image.ROTATE_180)
        elif orientation == 4:
            im.transpose(Image.FLIP_TOP_BOTTOM)
        elif orientation == 5:
            im.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 6:
            im.transpose(Image.ROTATE_270)
        elif orientation == 7:
            im.transpose(Image.ROTATE_90).transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 8:
            im.transpose(Image.ROTATE_90)
        else:
            pass

            # 重新修正Orientation值
            # im['Orientation'] = 1

    return im


def image_mogr_strip(im):
    """
    去除图片中的元信息
    :rtype : Image
    :param im:
    """
    return im


def image_mogr_thumbnail(im, image_size_geometry):
    """
    图像缩放
    :rtype : Image
    :param image_size_geometry:
    :param im:
    """
    if re.match(r"^!([1-9][0-9]*)p$", image_size_geometry):
        # /thumbnail/!<Scale>p
        # 基于原图大小，按指定百分比缩放。取值范围0-1000。
        scale = int(image_size_geometry[1:-1])
        if scale >= 1000:
            return
        im = im.resize(tuple(int(x * scale / 100) for x in im.size))
    elif re.match(r"^!([1-9][0-9]*)px$", image_size_geometry):
        # /thumbnail/!<Scale>px
        # 以百分比形式指定目标图片宽度，高度不变。取值范围0-1000。
        scale = int(image_size_geometry[1:-2])
        if scale >= 1000:
            return
        size = im.size
        resize = (int(size[0] * scale / 100), size[1])
        im = im.resize(resize)
    elif re.match(r"^!x([1-9][0-9]*)p$", image_size_geometry):
        # /thumbnail/!x<Scale>p
        # 以百分比形式指定目标图片高度，宽度不变。取值范围0-1000。
        scale = int(image_size_geometry[2:-1])
        if scale >= 1000:
            return
        size = im.size
        resize = (size[0], int(size[1] * scale / 100))
        im = im.resize(resize)
    elif re.match(r"^([1-9][0-9]*)x$", image_size_geometry):
        # /thumbnail/<Width>x
        # 指定目标图片宽度，高度等比缩放。取值范围0-10000。
        width = int(image_size_geometry[:-1])
        if width >= 10000:
            return
        size = im.size
        ratio = width / size[0]
        resize = (width, int(size[1] * ratio))
        im = im.resize(resize)
    elif re.match(r"^x([1-9][0-9]*)$", image_size_geometry):
        # /thumbnail/x<Height>
        # 指定目标图片高度，宽度等比缩放。取值范围0-10000。
        height = int(image_size_geometry[1:])
        if height >= 10000:
            return
        size = im.size
        ratio = height / size[1]
        resize = (int(size[0] * ratio), height)
        im = im.resize(resize)
    elif re.match(r"^([1-9][0-9]*)x([1-9][0-9]*)$", image_size_geometry):
        # /thumbnail/<Width>x<Height>
        # 限定长边，短边自适应缩放，将目标图片限制在指定宽高矩形内。
        # 取值范围不限，但若宽高超过10000只能缩不能放。
        image_size_geometry = [int(x) for x in image_size_geometry.split("x")]
        if min(image_size_geometry) > 10000:
            return

        size = im.size
        long_edge = max(size)
        short_edge = min(size)
        if max(size) > 10000:
            # 只能缩不能放
            ratio_w = image_size_geometry[0] / long_edge
            ratio_h = image_size_geometry[1] / short_edge
            ratio = min(ratio_w, ratio_h)
            if ratio >= 1:  # 只缩不放
                return
            else:
                resize = tuple(int(x * ratio) for x in size)
                im = im.resize(resize)
        else:
            ratio_w = image_size_geometry[0] / long_edge
            ratio_h = image_size_geometry[1] / short_edge
            ratio = min(ratio_w, ratio_h)
            resize = tuple(int(x * ratio) for x in size)
            if max(resize) > 10000:
                return
            im = im.resize(resize)
    elif re.match(r"^!([1-9][0-9]*)x([1-9][0-9]*)r$", image_size_geometry):
        # /thumbnail/!<Width>x<Height>r
        # 限定短边，长边自适应缩放，目标图片会延伸至指定宽高矩形外。
        # 取值范围不限，但若宽高超过10000只能缩不能放。
        image_size_geometry = [int(x) for x in image_size_geometry[1:-1].split("x")]
        if min(image_size_geometry) > 10000:
            return

        size = im.size
        long_edge = max(size)
        short_edge = min(size)
        if max(size) > 10000:
            # 只能缩不能放
            ratio_w = image_size_geometry[0] / long_edge
            ratio_h = image_size_geometry[1] / short_edge
            ratio = max(ratio_w, ratio_h)
            if ratio >= 1:  # 只缩不放
                return
            else:
                resize = tuple(int(x * ratio) for x in size)
                im = im.resize(resize)
        else:
            ratio_w = image_size_geometry[0] / long_edge
            ratio_h = image_size_geometry[1] / short_edge
            ratio = max(ratio_w, ratio_h)
            resize = tuple(int(x * ratio) for x in size)
            if max(resize) > 10000:
                return
            im = im.resize(resize)
    elif re.match(r"^([1-9][0-9]*)x([1-9][0-9]*)!$", image_size_geometry):
        # /thumbnail/<Width>x<Height>!
        # 限定目标图片宽高值，忽略原图宽高比例，按照指定宽高值强行缩略，可能导致目标图片变形。
        # 取值范围不限，但若宽高超过10000只能缩不能放。
        image_size_geometry = [int(x) for x in image_size_geometry[:-1].split("x")]
        if min(image_size_geometry) >= 10000:
            return
        im = im.resize(tuple(image_size_geometry))
    elif re.match(r"^([1-9][0-9]*)x([1-9][0-9]*)>$", image_size_geometry):
        # fix
        # /thumbnail/<Width>x<Height>>
        # 当原图尺寸大于给定的宽度或高度时，按照给定宽高值缩小。
        # 取值范围不限，但若宽高超过10000只能缩不能放。
        image_size_geometry = [int(x) for x in image_size_geometry[:-1].split("x")]
        if min(image_size_geometry) >= 10000:
            return

        size = im.size
        if size[0] < image_size_geometry[0] and size[1] < image_size_geometry[1]:
            ratio_w = image_size_geometry[0] / size[0]
            ratio_h = image_size_geometry[1] / size[1]
            ratio = min(ratio_w, ratio_h)
            resize = tuple(int(x * ratio) for x in size)
            im = im.resize(resize)
    elif re.match(r"^([1-9][0-9]*)x([1-9][0-9]*)<$", image_size_geometry):
        # fix
        image_size_geometry = [int(x) for x in image_size_geometry[:-1].split("x")]
        if min(image_size_geometry) >= 10000:
            return

        size = im.size
        if size[0] > image_size_geometry[0] and size[1] > image_size_geometry[1]:
            ratio_w = image_size_geometry[0] / size[0]
            ratio_h = image_size_geometry[1] / size[1]
            ratio = min(ratio_w, ratio_h)
            resize = tuple(int(x * ratio) for x in size)
            im = im.resize(resize)
    elif re.match(r"^([1-9][0-9]*)@$", image_size_geometry):
        # fix
        area = int(image_size_geometry[:-1])
        if area > 100000000:
            return

        size = im.size
        origin_area = size[0] * size[1]
        ratio = area / origin_area
        resize = tuple(int(x * ratio) for x in size)
        im = im.resize(resize)

    return im


def _get_gravity_point(size, gravity):
    point = [0, 0]
    if "NorthWest" == gravity:
        point[0] = 0
        point[1] = 0
    elif "North" == gravity:
        point[0] = int(size[0] / 2)
        point[1] = 0
    elif "NorthEast" == gravity:
        point[0] = size[0]
        point[1] = 0
    elif "West" == gravity:
        point[0] = 0
        point[1] = int(size[1] / 2)
    elif "Center" == gravity:
        point[0] = int(size[0] / 2)
        point[1] = int(size[1] / 2)
    elif "East" == gravity:
        point[0] = size[0]
        point[1] = int(size[1] / 2)
    elif "SouthWest" == gravity:
        point[0] = 0
        point[1] = size[1]
    elif "South" == gravity:
        point[0] = int(size[0] / 2)
        point[1] = size[1]
    elif "SouthEast" == gravity:
        point[0] = size[0]
        point[1] = size[1]

    return point


def get_box(size, point, width, height, dx=0, dy=0):
    """
    先趋于中心，后偏移。但是始终在原图范围内

    :param size: 数组size[0]底层背景的宽，size[1]底层背景的高
    :param point: 中心圆点坐标，左上角为0,0，右下角为size[0],size[1]
    :param width: 绿色图层的宽
    :param height: 绿色图层的高
    :param dx: 向右偏移量
    :param dy: 向下偏移量
    :return:
    """
    width = min(size[0], width)
    height = min(size[1], height)
    box = [int(point[0] - width / 2), int(point[1] - height / 2), int(point[0] + width / 2), int(point[1] + height / 2)]
    if box[0] < 0:
        # 先给box[2]赋值，它依赖于box[0]
        box[2] -= box[0]
        box[0] = 0
    if box[1] < 0:
        box[3] -= box[1]
        box[1] = 0

    # 因为width和height永远小于等于外层box的宽和高，上下两种情况不会同时出现
    # box[0] < 0 和 box[2] > size[0]不会同时存在
    if box[2] > size[0]:
        box[0] -= (box[2] - size[0])
        box[2] = size[0]
    if box[3] > size[1]:
        box[1] -= (box[3] - size[1])
        box[3] = size[1]

    if box[2] + dx > size[0]:
        box[0] += (size[0] - box[2])
        box[2] = size[0]
    if box[3] + dy > size[1]:
        box[1] += (size[1] - box[3])
        box[1] = size[1]

    return tuple(box)


def image_mogr_crop(im, gravity, crop):
    """
    图片裁剪
    """
    size = im.size
    point = _get_gravity_point(size, gravity)

    if re.match(r"^([1-9][0-9]*)x$", crop):
        width = int(crop[:-1])
        if width >= 10000:
            return

        box = get_box(size, point, width, size[1])
        im = im.crop(box)

    elif re.match(r"^x([1-9][0-9]*)$", crop):
        height = int(crop[1:])
        if height >= 10000:
            return

        box = get_box(size, point, size[0], height)
        im = im.crop(box)

    elif re.match(r"^([1-9][0-9]*)x([1-9][0-9]*)$", crop):
        crop = [int(x) for x in crop.split("x")]
        if min(crop) >= 10000:
            return

        box = get_box(size, point, crop[0], crop[1])
        im = im.crop(box)

    elif re.match(r"^!([1-9][0-9]*)x([1-9][0-9]*)a([1-9][0-9]*)a([1-9][0-9]*)$", crop):
        # /crop/!{cropSize}a<dx>a<dy>
        # 相对于偏移锚点，向右偏移dx个像素，同时向下偏移dy个像素。
        crop = [int(x) for x in re.findall(r"[1-9][0-9]*", crop)]
        if min(crop[:2]) >= 10000:
            return

        # point[0] += crop[2]
        # point[1] += crop[3]
        box = get_box(size, point, crop[0], crop[1], crop[2], crop[3])

        im = im.crop(box)

    elif re.match(r"^!([1-9][0-9]*)x([1-9][0-9]*)-([1-9][0-9]*)a([1-9][0-9]*)$", crop):
        # /crop/!{cropSize}-<dx>a<dy>
        # 相对于偏移锚点，向下偏移dy个像素，同时从指定宽度中减去dx个像素。
        crop = [int(x) for x in re.findall(r"[1-9][0-9]*", crop)]
        if min(crop[:2]) >= 10000:
            return

        # point[1] += crop[3]
        box = get_box(size, point, crop[0] - crop[2], crop[1], dy=crop[3])
        im = im.crop(box)

    elif re.match(r"^!([1-9][0-9]*)x([1-9][0-9]*)a([1-9][0-9]*)-([1-9][0-9]*)$", crop):
        # /crop/!{cropSize}a<dx>-<dy>
        # 相对于偏移锚点，向右偏移dx个像素，同时从指定高度中减去dy个像素。
        crop = [int(x) for x in re.findall(r"[1-9][0-9]*", crop)]
        if min(crop[:2]) >= 10000:
            return

        # point[0] += crop[2]
        box = get_box(size, point, crop[0], crop[1] - crop[3], dx=crop[2])
        im = im.crop(box)

    elif re.match(r"^!([1-9][0-9]*)x([1-9][0-9]*)-([1-9][0-9]*)-([1-9][0-9]*)$", crop):
        # /crop/!{cropSize}-<dx>-<dy>
        # 相对于偏移锚点，从指定宽度中减去dx个像素，同时从指定高度中减去dy个像素。
        crop = [int(x) for x in re.findall(r"[1-9][0-9]*", crop)]
        if min(crop[:2]) >= 10000:
            return

        box = get_box(size, point, crop[0] - crop[2], crop[1] - crop[3])
        im = im.crop(box)

    return im


def image_mogr_rotate(im, rotate_degree):
    # 旋转角度
    # 取值范围1-360，缺省为不旋转。
    rotate_degree = int(rotate_degree)
    if rotate_degree < 1 or rotate_degree > 360:
        return
    return im.rotate(rotate_degree)


def image_mogr_blur(im):
    # 高斯模糊
    return im.filter(ImageFilter.BLUR)


def _re_point(size, point, fontsize, dx=0, dy=0):
    """
    :param size:
    :param point:
    :param dx: 横轴边距
    :param dy: 纵轴边距
    :return:
    """
    if point[0] - dx < 0:
        point[0] += dx
    else:
        point[0] -= (fontsize[0] + dx)

    if point[1] - dy < 0:
        point[1] += dy
    else:
        point[1] -= (fontsize[1] + dy)

    return tuple(point)


def image_water_mark_text(im, text, font="黑体", fontsize=0, fill="white", dissolve=100,
                          gravity="SouthEast", dx=10, dy=10):
    try:
        font = ImageFont.truetype(fonts.fonts[font], int(fontsize))
    except IOError:
        raise

    try:
        fill = ImageColor.getrgb(fill)
    except ValueError:
        raise

    size = im.size
    point = _get_gravity_point(size, gravity)
    re_point = _re_point(size, point, font.getsize(text), dx, dy)
    draw = ImageDraw.Draw(im)
    draw.text(point, text.decode('utf-8'), fill=fill, font=font)
    return im