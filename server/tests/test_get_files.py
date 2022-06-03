import os

import pytest

from server.FileService import get_files


@pytest.mark.parametrize('create_list_file', [(
        ('tmp1', '111'),
        ('tmp2', '222')
)], indirect=True)
def test_get_file_data(create_list_file):
    os.chdir(create_list_file)
    result = get_files()
    assert isinstance(result, list) and all(isinstance(item, dict) and len(item.keys()) == 4 for item in result)
