#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, errno
from bson import objectid

UPLOAD_DIR = 'upload/'

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def generate_filepath(filename):
    file_id = objectid.ObjectId()
    ext = os.path.splitext(filename)[1]
    new_name = str(file_id) + ext
    file_dir = UPLOAD_DIR + file_id.generation_time.strftime("%Y%m%d")
    mkdir_p(file_dir)

    return file_dir, new_name

def get_filepath(filename, ext):
    if not objectid.ObjectId.is_valid(filename):
        return

    return UPLOAD_DIR + objectid.ObjectId(filename).generation_time.strftime("%Y%m%d") + "/" + filename + "." + ext
