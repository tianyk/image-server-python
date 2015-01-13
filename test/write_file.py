#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, errno

name = "lisi"


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


mkdir_p("e:/lisi/lisi")

with open("e:/lisi/lisi/lisi.txt", "w") as f:
    f.write(name)

# os.removedirs("e:/lisi/lisi")

