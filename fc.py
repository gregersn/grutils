#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import os
import hashlib
import argparse


def init_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("folder", nargs='+',
                        help="Folder(s) with files to compare")
    parser.add_argument("--ext", nargs='*',
                        help="Extensions to include")

    return parser


def find_files(folder, extensions=None):
    found_files = []
    for root, dirs, files in os.walk(folder):
        for filename in files:
            fullname = os.path.join(root, filename)
            if extensions is None:
                found_files.append(fullname)
            else:
                ext = os.path.splitext(fullname)[1][1:]
                if ext.lower() in extensions:
                    found_files.append(fullname)
    return found_files


def hash(file):
    hasher = hashlib.md5()
    with open(file, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def find_sizes(files):
    sizes = {}
    for file in files:
        statinfo = os.stat(file)
        size = statinfo.st_size

        if size not in sizes:
            sizes[size] = []

        sizes[size].append(file)

    return sizes


def find_hashes(files):
    hashes = {}
    for file in files:
        h = hash(file)
        if h not in hashes:
            hashes[h] = []

        hashes[h].append(file)

    return hashes


def main():
    parser = init_parser()
    args = parser.parse_args()

    files = []
    for folder in args.folder:
        print(" * Finding files in folder: ", folder)
        files += find_files(folder, args.ext)

    print("* Finding file sizes for %d files " % (len(files)))
    sizes = find_sizes(files)

    files = []
    for size in sizes:
        if len(sizes[size]) > 1:
            files += sizes[size]

    print(" * Finding hashes for %d files" % (len(files), ))
    hashes = find_hashes(files)
    duplicates = []
    for h in hashes:
        if len(hashes[h]) > 1:
            duplicates.append(hashes[h])

    if len(duplicates) > 0:
        print("* FOUND DUPLICATES * ")
        for duplicate in duplicates:
            print("Duplicate files: ")
            for file in duplicate:
                print(file)
    else:
        print("Found no duplicates")

if __name__ == '__main__':
    main()
