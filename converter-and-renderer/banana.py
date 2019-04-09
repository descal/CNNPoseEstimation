#!/usr/bin/env python3

import numpy as np
import re
from bananaApp import BananaApp
import cv2

def look():
    BananaApp.run_in_window()

def peel(N,d):
    bananaApp = BananaApp()
    for i in range(N):
        v = np.random.rand(3) * 2 - 1.0
        # print(v)
        # v[2] = 0
        # v[1] = 0
        v = v / np.linalg.norm(v) * d
        # v= 20, -10.0, 00.0
        r = np.random.rand() * 360
        # r = 90
        bananaApp.set_view_from_target(v, bananaApp.target, r)
        bananaApp.run_instance()

def changeBackground(imgPathIn,backPathIn,imgPathOut):
    imgFront = cv2.imread(imgPathIn) #'output/annotated_0006.png'
    imgBack = cv2.imread(backPathIn) #'plantation.jpg'

    height, width = imgFront.shape[:2]

    resizeBack = cv2.resize(imgBack, (width, height), interpolation=cv2.INTER_CUBIC)

    for i in range(width):
        for j in range(height):
            pixel = imgFront[j, i]
            if np.all(pixel == [0, 0, 0]):
                imgFront[j, i] = resizeBack[j, i]

    cv2.imwrite(imgPathOut,imgFront)
    return


def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(f):
    return [ tryint(c) for c in re.split('([0-9]+)', f.name) ]


def flatten(l): return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]


def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Go, Go, Bananas!!!')
    subparsers = parser.add_subparsers(dest='task', title='Tasks', help='What to do with bananas?')
    subparsers.required = True


    parser_interact = subparsers.add_parser('look', help='Render banana using an interactive window')


    parser_random = subparsers.add_parser('peel', help='Render banana from N random camera poses')
    parser_random.add_argument('N', type=int, help='Number of random poses')
    parser_random.add_argument('-d', metavar='distance', type=float, default=50, help='Camera distance from world origin')



    parser_cmd = subparsers.add_parser('chop', help='Render banana from given camera pose')

    parser_cmd_group1 = parser_cmd.add_argument_group('position')
    parser_cmd_group1.add_argument('x', type=float, help='Camera x-position')
    parser_cmd_group1.add_argument('y', type=float, help='Camera y-position')
    parser_cmd_group1.add_argument('z', type=float, help='Camera z-position')

    parser_cmd_group2 = parser_cmd.add_argument_group('orientation')
    parser_cmd_group2.add_argument('orientation', nargs='?', type=float, metavar='qx qy qz qw', action='append',  help='Camera orientation as quaternion')
    parser_cmd_group2.add_argument('orientation', nargs='?', type=float, metavar='roll pitch yaw', action='append',  help='Camera orientation in euler angles')
    parser_cmd_group2.add_argument('orientation', nargs=argparse.REMAINDER, type=float, action='append', help=argparse.SUPPRESS)



    parser_read = subparsers.add_parser('eat', help='Render banana from given pose files')
    parser_read.add_argument('file', nargs='+', type=argparse.FileType('r'), help='File names containing a camera pose')


    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    # print(args)

    if args.task == 'look':
        BananaApp.run_in_window()

    if args.task == 'peel':
        bananaApp = BananaApp()
        for i in range(args.N):
            v = np.random.rand(3)*2-1.0
            print(v)
            v[2]=0
            v = v / np.linalg.norm(v) * args.d
            # v= 20, -10.0, 00.0
            r = np.random.rand() * 360
            r=90
            bananaApp.set_view_from_target(v , bananaApp.target, r)
            bananaApp.run_instance()

    if args.task == 'chop':
        bananaApp = BananaApp()

        if args.orientation[0] is not None:
            orientation = flatten(args.orientation)
            if len(orientation) == 3:
                bananaApp.set_view_from_euler([args.x, args.y, args.z], orientation)
            elif len(orientation) == 4:
                bananaApp.set_view_from_quaternion([args.x, args.y, args.z], orientation)
            else:
                print('Wrong number of arguments', file=sys.stderr)
                parser.print_help(sys.stderr)
                sys.exit(1)
        else:
            bananaApp.set_view_from_target([args.x, args.y, args.z], bananaApp.target, bananaApp.roll)
        bananaApp.run_instance()

    if args.task == 'eat':
        bananaApp = BananaApp()
        args.file.sort(key=alphanum_key)
        for file in args.file:
            for line in file:
                line = line.strip()
                if not line: continue
                pose = np.fromstring(line, sep=' ')
                if len(pose[3:]) == 3:
                    bananaApp.set_view_from_euler(pose[:3], pose[3:])
                elif len(pose[3:]) == 4:
                    bananaApp.set_view_from_quaternion(pose[:3], pose[3:])
                print('Rendering for {}: {}, {}'.format(file.name, pose[:3], pose[3:]))
                bananaApp.run_instance()



if __name__ == "__main__":
    main()
