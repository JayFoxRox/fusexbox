#!/usr/bin/env python3

#FIXME: Add license

# See README.md for license information


#FIXME: Probably not necessary?
from __future__ import print_function, absolute_import, division

import logging

import array, fcntl, struct, termios, os

from fusexbox import *

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    with open(args.file, 'rb') as file:
      buf = array.array('h', [0])
      fcntl.ioctl(file, XBOXIOCRUN, buf, 1)
