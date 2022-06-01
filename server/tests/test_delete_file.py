import os

from server.FileService import delete_file


def test_delete_file():
    check_list = ['tmp1', 'tmp2', 'asfafasf']
    current_folder = os.path.dirname((os.path.abspath(__file__)))
    for file in check_list:
        tmp_file = open(file, 'w')
        tmp_file.close()
        delete_file(file)
        file_is_del = not os.path.exists(os.path.join(current_folder, file))
        if not file_is_del:
            os.remove(os.path.join(current_folder, file))
        assert file_is_del
