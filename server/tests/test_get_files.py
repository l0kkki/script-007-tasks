import os

from server.FileService import get_files


def test_get_file_data():
    check_list = ['tmp1', 'tmp2', 'asfafasf']
    current_folder = os.getcwd()
    for full_path in [os.path.join(current_folder, file) for file in check_list]:
        tmp_file = open(full_path, 'w')
        tmp_file.close()
    result = get_files()
    for full_path in [os.path.join(current_folder, file) for file in check_list]:
        if os.path.exists(full_path):
            os.remove(full_path)
    assert isinstance(result, list) and all(isinstance(item, dict) and len(item.keys()) == 4 for item in result)
