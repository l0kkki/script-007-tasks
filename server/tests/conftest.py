import pytest
import os
import shutil
import multiprocessing
from time import sleep


from config import Config
from server.WebHandler import WebHandler

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

tmp_test_folder = 'tmp_test'


def create_file(file, content):
    with open(file, 'w') as tmp_file:
        tmp_file.write(content)


@pytest.fixture(scope='function')
def tmp_dir_handler():
    current_folder = os.path.dirname((os.path.abspath(__file__)))
    test_folder_path = os.path.join(current_folder, tmp_test_folder)
    if not os.path.exists(test_folder_path):
        os.mkdir(test_folder_path)
    yield test_folder_path
    os.chdir(current_folder)
    if os.path.exists(test_folder_path):
        shutil.rmtree(test_folder_path)


@pytest.fixture(scope='function')
def create_single_file(request, tmp_dir_handler):
    file_name, content = request.param
    full_path = os.path.join(tmp_dir_handler, file_name)
    create_file(full_path, content)
    yield full_path


@pytest.fixture(scope='function')
def create_list_file(request, tmp_dir_handler):
    file_arg_list = request.param
    for file_arg in file_arg_list:
        full_path = os.path.join(tmp_dir_handler, file_arg[0])
        create_file(full_path, file_arg[1])
    yield tmp_dir_handler


@pytest.fixture(scope='function')
def run_web_app(tmp_dir_handler, unused_tcp_port_factory):

    config = Config(TEST_DIR, get_cli_arg=False).config
    config['directory'] = tmp_dir_handler
    config['port'] = unused_tcp_port_factory()
    wh = WebHandler(config)
    server_process = multiprocessing.Process(target=wh.run_web_application)
    server_process.start()
    sleep(5)
    yield f'http://{config["host"]}:{config["port"]}'
    server_process.terminate()
    server_process.join(5)
