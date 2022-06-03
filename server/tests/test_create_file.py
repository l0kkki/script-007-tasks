import os

import pytest

from server.FileService import create_file


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
