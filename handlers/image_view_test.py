#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from base_image import BaseImageHandler

class ImageViewTestHandler(BaseImageHandler):
    def get(self):
        interface = self.get_argument("interface", None)
        mode      = self.get_argument("mode", None)
        w         = self.get_argument("w", None)
        h         = self.get_argument("h", None)

        resp = "resp: "
        if interface:
            resp += (",interface: " + interface)
        if mode:
            resp += (",mode: " + mode)
        if w:
            resp += (",w: " + w)
        if h:
            resp += (",h: " + h)

        self.write(resp)
