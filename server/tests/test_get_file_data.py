import pytest

from server.FileService import get_file_data


@pytest.mark.parametrize('create_single_file', [('tmp1', '111')], indirect=True)
def test_get_file_data(create_single_file):
    result = get_file_data(create_single_file)
    assert isinstance(result, dict) and len(result.keys()) == 5
