#!/usr/bin/env python
"""
@author: moloch
Copyright 2018
"""

import os
import sys
import logging

from english2bin import Binary2DictlessEnglish

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.options import define, options


define("target",
       group="application",
       default=os.environ.get('WIRE_TRANSFER_TARGET', "shell.exe"),
       help="target file to transfer")

define("dictionary",
       group="application",
       default=os.environ.get('WIRE_TRANSFER_DICTIONARY', "dictionary.txt"),
       help="encode file with dictionary")

define("listen_port",
       group="application",
       default=os.environ.get('WIRE_TRANSFER_LPORT', 8888),
       type=int,
       help="listen port")

define("debug",
       default=os.environ.get('WIRE_TRANSFER_DEBUG', False),
       group="application",
       help="start the application in debugging mode",
       type=bool)


class MainHandler(RequestHandler):

    def initialize(self):
        self.encoder = self.application.settings['encoder']

    def get(self):
        with open(options.target, "rb") as fp:
            data = self.encoder.encode_file(fp)
        self.render("templates/legit.html", data=data)

def make_app():
    return Application([
        (r"/", MainHandler),
        (r"/static/(.*)", StaticFileHandler, {"path": "./static/"}),
    ], encoder=Binary2DictlessEnglish(options.dictionary))


def main():
    """ Starts the app based on cli arguments """

    if options.debug:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
    
    app = make_app()
    app.listen(options.listen_port)
    IOLoop.current().start()


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        options.parse_command_line()
        assert os.path.exists(options.target)
        assert os.path.exists(options.dictionary)
        main()
    except IOError as error:
        print(str(error))
        sys.exit()