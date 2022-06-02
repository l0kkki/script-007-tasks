import os

import pytest

from server.FileService import change_dir


@pytest.mark.parametrize(
    'folder_name', ['tmp1', 'tmp2', 'tmp3']
)
def test_change_dir(folder_name, tmp_dir_handler):
    full_path = os.path.join(tmp_dir_handler, folder_name)
    change_dir(full_path)
    assert os.getcwd() == full_path
