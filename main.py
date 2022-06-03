#!/usr/bin/env python3
import logging
import logging.config
import sys

from aiohttp import web

from server.WebHandler import WebHandler
from utils.Config import config


def setup_logger(level='NOTSET', filename=None):
    logger_conf = {
        'version': 1,
        'formatters': {
            'default': {
                'format':
                    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': level,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
    if filename:
        logger_conf['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'encoding': 'UTF-8',
            'formatter': 'default',
            'filename': filename,
        }
        logger_conf['root']['handlers'].append('file')
    logging.config.dictConfig(logger_conf)


def main():
    setup_logger(level=logging.getLevelName(config.log.level.upper()),
                 filename=config.log.file)
    logging.debug('started')
    logging.debug('config %s', config.to_dict())

    handler = WebHandler()
    app = web.Application()
    app.add_routes([
        web.get('/', handler.handle),
        # TODO: add more routes
    ])
    web.run_app(app, port=config.port)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\nERROR: Interrupted by user', file=sys.stderr)
        sys.exit(1)
    except BaseException as err:
        print(f'ERROR: Something goes wrong:\n{err}', file=sys.stderr)
        sys.exit(1)
