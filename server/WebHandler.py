import json
import logging
import os

from aiohttp import web

import server.FileService as FileService
import server.Utils as Utils


class WebHandler:
    """aiohttp handler with coroutines."""

    def __init__(self, config: dict) -> None:
        self.config = config
        FileService.change_dir(self.config['directory'])
        self.app = web.Application()
        self.init_routes()

    def run_web_application(self):
        """ Run server """
        web.run_app(self.app, host=self.config['host'], port=self.config['port'])

    def init_routes(self):
        """ Init routes for app """
        self.app.add_routes([web.get('/', self.handle)])
        self.app.add_routes([web.get('/change_dir/{dir}', self.change_dir)])
        self.app.add_routes([web.get('/files', self.get_files)])
        self.app.add_routes([web.get('/info/{file}', self.get_file_data)])
        self.app.add_routes([web.post('/create', self.create_file)])
        self.app.add_routes([web.delete('/delete/{file}', self.delete_file)])
        logging.debug('Routes added')

    @staticmethod
    async def handle(request: web.Request) -> web.Response:
        """Basic coroutine for connection testing.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with status.
        """

        logging.debug(f'Basic handle {request}')

        return web.json_response(data={
            'status': 'success',
            'work_dir': os.getcwd()
        })

    @staticmethod
    async def change_dir(request: web.Request) -> web.Response:
        """Coroutine for changing working directory with files.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "path": "string. Directory path. Required",
            }.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """
        logging.debug(f'Incoming {request}')
        dir_path = request.match_info.get('dir', '.')
        FileService.change_dir(dir_path)
        return web.json_response(data={
            'status': 'success',
            'work_dir': os.getcwd()
        })

    @staticmethod
    async def get_files(request: web.Request) -> web.Response:
        """Coroutine for getting info about all files in working directory.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with success status and data or error status and error message.
        """
        logging.debug(f'Incoming {request}')
        result = FileService.get_files()
        return web.json_response(data={'status': 'success', 'files': result},
                                 dumps=lambda x: json.dumps(x, default=str))

    @staticmethod
    async def get_file_data(request: web.Request) -> web.Response:
        """Coroutine for getting full info about file in working directory.

        Args:
            request (Request): aiohttp request, contains filename and is_signed parameters.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        logging.debug(f'Incoming {request}')
        file_path = request.match_info.get('file')
        result = FileService.get_file_data(file_path)
        web.json_response()
        return web.json_response(data={'status': 'success', 'file_info': result},
                                 dumps=lambda x: json.dumps(x, default=str))

    @staticmethod
    async def create_file(request: web.Request) -> web.Response:
        """Coroutine for creating file.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                'filename': 'string. filename',
                'content': 'string. Content string. Optional',
            }.

        Returns:
            Response: JSON response with success status and data or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.
        """

        logging.debug(f'Incoming {request}')
        request_json = await Utils.get_json_from_request(request)
        file = request_json.get('file')
        content = request_json.get('content')
        result = FileService.create_file(file, content)
        return web.json_response(data={'status': 'success', 'file_info': result},
                                 dumps=lambda x: json.dumps(x, default=str))

    @staticmethod
    async def delete_file(request: web.Request) -> web.Response:
        """Coroutine for deleting file.

        Args:
            request (Request): aiohttp request, contains filename.

        Returns:
            Response: JSON response with success status and success message or error status and error message.

        Raises:
            HTTPBadRequest: 400 HTTP error, if error.

        """

        logging.debug(f'Incoming {request}')
        file_path = request.match_info.get('file')
        FileService.delete_file(file_path)
        return web.json_response(data={
            'status': 'success'
        })
