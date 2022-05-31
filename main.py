#!/usr/bin/env python3
import os
import argparse

from server import FileService


def main():
    default_wd = os.path.dirname(os.path.abspath(__file__))
    default_wd = os.path.join(default_wd, r'FileServer')
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--directory',
                        help='Path to working directory',
                        default=default_wd)
    cmd_params = parser.parse_args()
    FileService.change_dir(cmd_params.directory)


if __name__ == '__main__':
    main()
