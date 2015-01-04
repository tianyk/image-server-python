#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import re
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import handlers

from tornado.options import define, options
from handlers import HomeHandler, UploadHandler, PhotoHandler, ImageViewHandler, TestHandler, ImageViewTestHandler

tornado.options.parse_command_line()

define("port", default=8888, help="run on the given port", type=int)
# define("log_file_prefix", default="logs/tornado.log", help="logging_level")

#
class Application(tornado.web.Application):
    """docstring for Application"""
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/upload", UploadHandler),
            (r"/photos", PhotoHandler),
            (r"/(.+)\.(jpg|gif|png)", ImageViewHandler),
            (r"/test", TestHandler),
            (r"/img_view_test", ImageViewTestHandler)
        ]

        settings = dict(
            blog_title=u"Tornado Blog",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # ui_modules={"Entry": EntryModule},
            # xsrf_cookies=True,
            cookie_secret="Kxf0IS7jKl4EXzjUcT6CKs81cMfuz3",
            login_url="/auth/login",
            debug=True,
        )

        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print "Server running on", options.port
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()