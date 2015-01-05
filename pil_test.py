#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from PIL import Image, ImageDraw, ImageEnhance

# file_path = "./static/2850497089250002266.jpg"

# # 生成缩略图
# im = Image.open(file_path)
# w, h = im.size
# im.thumbnail((w//2, h//2), Image.ANTIALIAS)
# im.save(file_path + ".thumbnail" + ".jpg", "JPEG")

# # 旋转
# im = Image.open(file_path)
# im = im.rotate(15)
# # im.save(file_path + ".rotate" + ".jpg", 'JPEG')
# # im.show()

# # 创建一张图片
# im = Image.new("RGB", (512, 512), "white")
# # im.save('./static/new.jpg', "JPEG")
# # im.show()

# # 图片混合
# # Both images must have the same size and mode.两张图要有相同的大小和模式
# im1 = Image.open(file_path);
# im2 = Image.open('./static/1370220186728336813.jpg');
# im2 = im2.resize(im1.size)
# # alpha的取值从0到1，随着越来越大。第二张图片会越来越靠上层
# im3 = Image.blend(im1, im2, 0.3)
# # im3.show()

# # composite
# im1 = Image.open(file_path);
# im2 = Image.open('./static/1370220186728336813.jpg');
# im2 = im2.resize(im1.size)
# mask = Image.new('L', im1.size, 0)
# im3 = Image.composite(im1, im2, mask)
# # im3.show()

# background = Image.new('RGB', (100, 100), (255, 255, 255))
# # background.show()
# foreground = Image.new('RGB', (100, 100), (255, 0, 0))
# # foreground.show()
# mask = Image.new('L', (100, 100), 0)
# draw = ImageDraw.Draw(mask)
# for i in range(5, 100, 10):
#     draw.line((i, 0, i, 100), fill=random.randrange(256))
#     draw.line((0, i, 100, i), fill=random.randrange(256))
# # mask.show()
# result = Image.composite(background, foreground, mask)
# # result.show()

# # 色彩模式
# im = Image.open(file_path)
# im = im.convert('1')
# # im.show()
# im = Image.open(file_path)
# im = im.convert('L')
# # im.show()
# im = Image.open(file_path)
# im = im.convert('P')
# # im.show()
# im = Image.open(file_path)
# im = im.convert('RGB')
# # im.show()
# im = Image.open(file_path)
# im = im.convert('RGBA')
# # im.show()
# im = Image.open(file_path)
# im = im.convert('YCbCr')
# # im.show()
# im = Image.open(file_path)
# im = im.convert('I')
# # im.show()
# im = Image.open(file_path)
# im = im.convert('F')
# # im.show()
# im = Image.open(file_path)
# im = im.convert('LA')
# # im.show()
# im = Image.open(file_path)
# im = im.convert('RGBX')
# # im.show()

# # 图像处理 色彩、锐化、对比度、亮度
# im = Image.open("./static/6619229324002674138.png")
# # im.show()
# enhancer = ImageEnhance.Color(im)
# # 1 原图
# factor = 0
# for i in range(10):
#     print factor
#     # enhancer.enhance(factor).show()
#     factor += 0.1
# # im.show()
# #
# # 图片裁剪
# im = Image.open("./static/6619229324002674138.png")
# box = (100, 100, 400, 400)
# box_im = im.crop(box)
# box_im.show()
# # 旋转180度
# box_im = box_im.transpose(Image.ROTATE_180)
# box_im.show()
# im.paste(box_im, box)
# im.show()
# # Image.open("./static/6619229324002674138.png").show()
# #

im = Image.open("./upload/99723.jpg")
print im.format
print im.size
print im.mode


