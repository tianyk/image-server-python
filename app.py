#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from handlers import HomeHandler, UploadHandler, ImageViewHandler, TestHandler, ImageViewTestHandler, ParamTestHandler

define("port", default=8888, help="run on the given port", type=int)


#
class Application(tornado.web.Application):
    """docstring for Application"""

    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/upload", UploadHandler),
            (r"/(.+)\.(jpg|gif|png)", ImageViewHandler),
            (r"/param", ParamTestHandler)
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


if __name__ == "__main__":
    main()