import os
import logging
from datetime import datetime


def change_dir(path: str, autocreate: bool = True) -> None:
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.
        autocreate (bool): Create folder if it doesn't exist.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
        ValueError: if path is invalid.
    """

    if os.path.isdir(path):
        os.chdir(path)
        logging.debug(f'Directory changed to {path}')
    elif autocreate:
        try:
            logging.debug(f'Create directory on path {path}')
            os.mkdir(path)
        except Exception as ex:
            ex_text = 'Cant create directory, path {path}, base exception: {ex}'
            logging.error(ex_text)
            raise ValueError(ex_text)
        os.chdir(path)
        logging.debug(f'Directory changed to {path}')
    else:
        ex_text = 'Directory does not exist, autocreate is False'
        logging.error(ex_text)
        raise RuntimeError(ex_text)


def get_files() -> list:
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """

    cwd = os.getcwd()
    file_list = [elem for elem in os.listdir(cwd) if os.path.isfile(elem)]
    logging.debug(f'Returns file list in {cwd}')
    return [{'name': os.path.basename(file),
             'create_date': datetime.fromtimestamp(os.path.getctime(file)),
             'edit_date': datetime.fromtimestamp(os.path.getmtime(file)),
             'size': os.path.getsize(file)}
            for file in file_list]


def get_file_data(filename: str) -> dict:
    """Get full info about file.

    Args:
        filename (str): Filename.

    Returns:
        Dict, which contains full info about file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - edit_date (datetime): date of last file modification
        - size (int): size of file in bytes

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    try:
        logging.debug(f'Getting info from file {filename}')
        with open(filename, 'r') as file:
            content = file.read()
        return {'name': os.path.basename(filename),
                'content': content,
                'create_date': datetime.fromtimestamp(os.path.getctime(filename)),
                'edit_date': datetime.fromtimestamp(os.path.getmtime(filename)),
                'size': os.path.getsize(filename)}
    except FileNotFoundError:
        ex_text = f'File does not exist {filename}'
        logging.error(ex_text)
        raise RuntimeError(ex_text)
    except Exception:
        ex_text = f'Filename is invalid {filename}'
        logging.error(ex_text)
        raise ValueError(ex_text)


def create_file(filename: str, content: str = None) -> dict:
    """Create a new file.

    Args:
        filename (str): Filename.
        content (str): String with file content.

    Returns:
        Dict, which contains name of created file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - size (int): size of file in bytes

    Raises:
        ValueError: if filename is invalid.
    """

    try:
        logging.debug(f'Createing file {filename}')
        with open(filename, 'w') as file:
            if content is not None:
                file.write(content)
        return {'name': os.path.basename(filename),
                'content': content,
                'create_date': datetime.fromtimestamp(os.path.getctime(filename)),
                'size': os.path.getsize(filename)}
    except Exception:
        ex_text = f'Filename is invalid {filename}'
        logging.error(ex_text)
        raise ValueError(ex_text)


def delete_file(filename: str) -> None:
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    try:
        logging.debug(f'Deleting file {filename}')
        os.remove(filename)
    except FileNotFoundError:
        ex_text = f'File does not exist {filename}'
        logging.error(ex_text)
        raise RuntimeError(ex_text)
