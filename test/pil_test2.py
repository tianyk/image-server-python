#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageFile

image = Image.open("upload/P41116-164339.jpg")

try:
    image.save("upload/P41116-164339.jpg_2.jpg", "JPEG", quality=80, optimize=True, progressive=True)
except IOError:
    ImageFile.MAXBLOCK = image.size[0] * image.size[1]
    image.save("upload/P41116-164339.jpg_2.jpg", "JPEG", quality=80, optimize=True, progressive=True)

# print image._getexif()

from PIL.ExifTags import TAGS

# for k, v in image._getexif().items():
#     print TAGS.get(k, k), v
image = Image.open("upload/p1561863679.jpg")
if image._getexif():
    # dict(zip(d.keys(), map(lambda x:x * 2, d.values())))
    # dict((k, v*2) for k, v in {'a': 1, 'b': 2}.items())
    exif = dict((TAGS.get(k, k), v) for k, v in image._getexif().items())
    print exif
else:
    print None