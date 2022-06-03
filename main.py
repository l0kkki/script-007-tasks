#!/usr/bin/env python3
import os
import logging.handlers
import argparse
import sys

from server import FileService


def init_logging(log_dir, level):
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    log_file = os.path.join(log_dir, 'server.log')
    logging.basicConfig(level=level,
                        format='%(asctime)s %(levelname)-7s %(module)s.%(funcName)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[
                            logging.handlers.TimedRotatingFileHandler(filename=log_file, when='midnight'),
                            logging.StreamHandler(sys.stdout)])


def main():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    default_wd = os.path.join(main_dir, r'FileServer')
    default_log_dir = os.path.join(main_dir, r'Logs')
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--directory',
                        help='Path to working directory',
                        default=default_wd)
    parser.add_argument('--log_dir',
                        help='Path to logging directory',
                        default=default_log_dir)
    parser.add_argument('--log_level',
                        choices=[10, 20, 30, 40, 50],
                        type=int,
                        help='Logging level',
                        default=20)
    cmd_params = parser.parse_args()
    init_logging(cmd_params.log_dir, cmd_params.log_level)
    FileService.change_dir(cmd_params.directory)
    logging.info('Done')


if __name__ == '__main__':
    main()
