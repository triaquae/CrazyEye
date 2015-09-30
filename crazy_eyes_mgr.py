#_*_coding:utf-8_*_
__author__ = 'jieli'

import sys
basedir = '/'.join(__file__.split("/")[:-2])
sys.path.append(basedir)

from backend import main

if __name__ == '__main__':
    main.call(sys.argv[1:])