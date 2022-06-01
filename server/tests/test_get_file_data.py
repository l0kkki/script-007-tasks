import os

from server.FileService import get_file_data


def test_get_file_data():
    check_list = ['tmp1', 'tmp2', 'asfafasf']
    current_folder = os.path.dirname((os.path.abspath(__file__)))
    for file in check_list:
        tmp_file = open(file, 'w')
        tmp_file.close()
        result = get_file_data(file)
        if os.path.exists(os.path.join(current_folder, file)):
            os.remove(os.path.join(current_folder, file))
        assert isinstance(result, dict) and len(result.keys()) == 5
