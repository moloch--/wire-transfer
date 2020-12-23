#!/usr/bin/env python3
"""
@author: moloch
Copyright 2019
"""

import os
import sys
import logging

from english2bin import Binary2DictlessEnglish

from tornado.ioloop import IOLoop
from tornado.template import Template
from tornado.options import define, options


define("target",
       group="application",
       default=os.environ.get('WIRE_TRANSFER_TARGET', "shell.exe"),
       help="target file to transfer")

define("output",
       group="application",
       default=os.environ.get('WIRE_TRANSFER_OUTPUT', "legit-embed.html"),
       help="target file to transfer")

define("dictionary",
       group="application",
       default=os.environ.get('WIRE_TRANSFER_DICTIONARY', "dictionary.txt"),
       help="encode file with dictionary")

define("template",
       group="application",
       default=os.environ.get('WIRE_TRANSFER_TEMPLATE', "templates/embed.html"),
       help="encode file into embedable .html file")


def main():
    """ Starts the app based on cli arguments """
    encoder = Binary2DictlessEnglish(options.dictionary)
    with open(options.target, "rb") as in_file:
        data = encoder.encode_file(in_file)
    with open(options.template) as templ_file:
        templ = Template(templ_file.read())
    with open(options.output, "wb") as out_file:
        out_file.write(templ.generate(data=data))

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