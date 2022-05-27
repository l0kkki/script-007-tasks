# https://docs.pytest.org/en/latest/how-to/tmp_path.html#the-tmp-path-fixture
import os

import pytest

import utils.FileUtils


# tmp_path is build-in fixture in pytest
def test_create_file(tmp_path):
    print(f"1>{tmp_path}<")  # str(tmp_path), use -s to see output

    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    content = 'abcd'
    p.write_text(content)
    assert p.read_text() == content
    assert len(list(tmp_path.iterdir())) == 1


@pytest.fixture(scope='function')
def change_test_dir(tmp_path):
    with utils.FileUtils.remember_cwd():
        os.chdir(str(tmp_path))
        yield str(tmp_path)


def test_nothing(change_test_dir):
    print(f"2>{change_test_dir}<")  # another value of tmp_path
    print(f"3>{os.getcwd()}")
