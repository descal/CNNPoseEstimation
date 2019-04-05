#!/usr/bin/env python3

import argparse
import os

import d3.model.tools as mt
import functools as fc
from d3.model.basemodel import Vector

def check_path(path, should_exist):
    """ Check that a path (file or folder) exists or not and return it.
    """
    path = os.path.normpath(path)
    if should_exist != os.path.exists(path):
        msg = "path " + ("does not" if should_exist else "already") + " exist: " + path
        raise argparse.ArgumentTypeError(msg)
    return path

def main(input,output,file_type,from_up,to_up):

    if (from_up is None) != (to_up is None):
        raise Exception("from-up and to-up args should be both present or both absent")

    up_conversion = None
    if from_up is not None:
        up_conversion = (from_up, to_up)

    output = output if output is not None else '.' + file_type

    result = mt.convert(input, output, up_conversion)

    if output is None:
        print(result)
    else:
        with open(output, 'w') as f:
            f.write(result)

#if __name__ == '__main__':
#    parser = argparse.ArgumentParser()
#    parser.set_defaults(func=main)
#    parser.add_argument('-v', '--version', action='version', version='1.0')
#    parser.add_argument('-i', '--input', metavar='input',
#                        type=fc.partial(check_path, should_exist=True), default=None,
#                        help='Input file')
#    parser.add_argument('-o', '--output', metavar='output',
#                        help='Output path')
#    parser.add_argument('-t', '--type', metavar='type',
#                        help='Export type, useless if output is specified')
#    parser.add_argument('-fu', '--from-up', metavar='fup', default=None,
#                        help="Initial up vector")
#    parser.add_argument('-tu', '--to-up', metavar='fup', default=None,
#                        help="Output up vector")
#    args = parser.parse_args()
#    args.func(args)

