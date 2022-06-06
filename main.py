#!/usr/bin/env python3
import os
import logging.handlers
import sys

from config import Config
from server.WebHandler import WebHandler


MAIN_DIR = os.path.dirname(os.path.abspath(__file__))


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
    if 'conf_file_warning' in config:
        logging.warning(f'Cant read config.yaml, catch exception {config["conf_file_warning"]}')
    logging.info('Start file service')
    WebHandler(config).run_web_application()
    logging.info('Done')


if __name__ == '__main__':
    main()
