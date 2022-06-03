import os

import pytest

from server.FileService import delete_file


@pytest.mark.parametrize('create_single_file', [('tmp1', '111')], indirect=True)
def test_delete_file(create_single_file):
    delete_file(create_single_file)
    assert not os.path.exists(create_single_file)
