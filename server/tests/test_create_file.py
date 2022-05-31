import os

from server.FileService import create_file


def test_change_dir():
    check_dict = {'tmp1': '1111', 'tmp2': '222', 'asfafasf': None}
    current_folder = os.path.dirname((os.path.abspath(__file__)))
    for file in check_dict:
        result = create_file(file, check_dict[file])
        if os.path.exists(os.path.join(current_folder, file)):
            os.remove(os.path.join(current_folder, file))
        assert isinstance(result, dict)
