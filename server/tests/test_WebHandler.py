import pytest
import requests
import json


def test_handle(run_web_app):
    """ Test WebHandler.handle() """
    result = requests.get(url=f'{run_web_app}/').json()
    assert result['status'] == 'success'


@pytest.mark.parametrize(
    'folder_name', ['tmp1', 'tmp2', 'tmp3']
)
def test_change_dir(folder_name, run_web_app):
    """ Test WebHandler.change_dir() """
    result = requests.get(url=f'{run_web_app}/change_dir/{folder_name}').json()
    assert result['status'] == 'success'


@pytest.mark.parametrize('create_list_file', [(
        ('tmp1', '111'),
        ('tmp2', '222')
)], indirect=True)
def test_get_files(create_list_file, run_web_app):
    """ Test WebHandler.get_files() """
    result = requests.get(url=f'{run_web_app}/files').json()
    assert result['status'] == 'success'


@pytest.mark.parametrize('create_single_file', [('tmp1', '111')], indirect=True)
def test_get_file_data(create_single_file, run_web_app):
    """ Test WebHandler.get_file_data()"""
    result = requests.get(url=f'{run_web_app}/info/{create_single_file}').json()
    assert result['status'] == 'success'


@pytest.mark.parametrize(
    'file_name, content', [
        ('tmp1', '111'),
        ('tmp2', '222'),
        ('tmp3', '333')]
)
def test_create_file(file_name, content, run_web_app):
    """ Test WebHandler.create_file() """
    result = requests.post(url=f'{run_web_app}/create',
                           json={'file': file_name, 'content': content}).json()
    assert result['status'] == 'success'


@pytest.mark.parametrize('create_single_file', [('tmp1', '111')], indirect=True)
def test_delete_file(create_single_file, run_web_app):
    """ Test WebHandler.delete_file() """
    result = requests.delete(url=f'{run_web_app}/delete/{create_single_file}').json()
    assert result['status'] == 'success'
