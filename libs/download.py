#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'tyk'

import os
import urllib

from bson import objectid
TEMP_DIR = "temp/"
# def get_md5(full_filename):
#     f = file(full_filename, 'rb')
#     return md5.new(f.read()).hexdigest()
#
#
# def check_md5(correct_md5, full_filename):
#     my_md5 = get_md5(full_filename)
#     if my_md5.upper() == correct_md5.upper():
#         return True
#     else:
#         return False


def download_image(image_url):
    try:
        if not os.path.exists(TEMP_DIR):
            os.mkdir(TEMP_DIR)
    except:
        print "Failed to create directory in %s" % dir

    file_id = objectid.ObjectId()
    path = TEMP_DIR + "/" + str(file_id)
    reader = urllib.urlopen(image_url)
    writer = file(path, "wb")

    # @see http://stackoverflow.com/questions/1538617/http-download-very-big-file
    try:
        data = None
        while data != '':
            data = reader.read(1024)
            writer.write(data)
    finally:
        writer.close()
        reader.close()
        return

    return str(file_id)