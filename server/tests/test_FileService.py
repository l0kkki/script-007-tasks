import os

import pytest

from server.FileService import change_dir
from server.FileService import delete_file
from server.FileService import create_file
from server.FileService import get_file_data
from server.FileService import get_files


@pytest.mark.parametrize(
    'folder_name', ['tmp1', 'tmp2', 'tmp3']
)
def test_change_dir(folder_name, tmp_dir_handler):
    full_path = os.path.join(tmp_dir_handler, folder_name)
    change_dir(full_path)
    assert os.getcwd() == full_path


@pytest.mark.parametrize(
    'file_name, content', [
        ('tmp1', '111'),
        ('tmp2', '222'),
        ('tmp3', '333')]
)
def test_create_file(file_name, content, tmp_dir_handler):
    full_path = os.path.join(tmp_dir_handler, file_name)
    result = create_file(full_path, content)
    assert isinstance(result, dict)


@pytest.mark.parametrize('create_single_file', [('tmp1', '111')], indirect=True)
def test_delete_file(create_single_file):
    delete_file(create_single_file)
    assert not os.path.exists(create_single_file)


@pytest.mark.parametrize('create_single_file', [('tmp1', '111')], indirect=True)
def test_get_file_data(create_single_file):
    result = get_file_data(create_single_file)
    assert isinstance(result, dict) and len(result.keys()) == 5


@pytest.mark.parametrize('create_list_file', [(
        ('tmp1', '111'),
        ('tmp2', '222')
)], indirect=True)
def test_get_file_data(create_list_file):
    os.chdir(create_list_file)
    result = get_files()
    assert isinstance(result, list) and all(isinstance(item, dict) and len(item.keys()) == 4 for item in result)
