#!/usr/bin/env python3
import os
import logging.handlers
import sys

import pytest

from config import Config
from server import FileService


MAIN_DIR = main_dir = os.path.dirname(os.path.abspath(__file__))


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
    config = Config(MAIN_DIR).config
    init_logging(config['log_dir'], config['log_level'])
    logging.info('Start file service')
    FileService.change_dir(config['directory'])
    logging.info('Done')


if __name__ == '__main__':
    main()
