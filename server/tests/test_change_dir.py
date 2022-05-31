import os

from server.FileService import change_dir


def test_change_dir():
    check_list = ['tmp1', 'tmp2', 'asfafasf']
    current_folder = os.path.dirname((os.path.abspath(__file__)))
    for folder in check_list:
        change_dir(folder)
        result = os.getcwd()
        if os.path.exists(os.path.join(current_folder, folder)):
            os.chdir(current_folder)
            os.rmdir(os.path.join(current_folder, folder))
        assert result == os.path.join(current_folder, folder)
