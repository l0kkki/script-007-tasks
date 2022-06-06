import os
import argparse

import yaml


CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.yaml')


class Config:

    @staticmethod
    def get_config_from_cl():
        """ Get application params from CommandLine arguments

        Returns:
            Dict with non empty value:
             - directory
             - host
             - port
             - log_dir
             - log_level
        """

        parser = argparse.ArgumentParser()
        parser.add_argument('-d',
                            '--directory',
                            help='Path to working directory')
        parser.add_argument('--host',
                            help='Application host')
        parser.add_argument('-p',
                            '--port',
                            help='Application port')
        parser.add_argument('--log_dir',
                            help='Path to logging directory')
        parser.add_argument('--log_level',
                            choices=[10, 20, 30, 40, 50],
                            type=int,
                            help='Logging level'
                                 '10-DEBUG, 20-INFO, 30-WARNING, 40-ERROR, 50-CRITICAL')
        cmd_params = parser.parse_args().__dict__
        return {key: value for key, value in cmd_params.items() if value is not None}

    @staticmethod
    def get_config_from_env():
        """ Get application params from Environment arguments

        Returns:
            Dict with non empty value:
             - directory
             - host
             - port
             - log_dir
             - log_level
        """

        app_prefix = 'FILE_SERVER_'
        accord_dict = {
            f'{app_prefix}DIRECTORY': 'directory',
            f'{app_prefix}HOST': 'host',
            f'{app_prefix}PORT': 'port',
            f'{app_prefix}LOG_DIR': 'log_dir',
            f'{app_prefix}LOG_LEVEL': 'log_level'
        }
        return {accord_dict[key]: val for key, val in os.environ.items() if key in accord_dict and val is not None}

    @staticmethod
    def get_config_from_file():
        """ Get application params from config.yaml arguments

        Returns:
            Dict with non empty value:
             - directory
             - host
             - port
             - log_dir
             - log_level
        """
        yaml_conf = {}
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as conf_file:
                yaml_conf = yaml.load(conf_file, Loader=yaml.Loader)
        except Exception as ex:
            yaml_conf['conf_file_warning'] = ex
        return yaml_conf

    def __init__(self, main_dir):
        # default config
        self.config = {
            'directory': os.path.join(main_dir, 'FileServer'),
            'host': '127.0.0.1',
            'port': '80',
            'log_dir': os.path.join(main_dir, 'Logs'),
            'log_level': 20
        }
        self.config.update(self.get_config_from_file())
        self.config.update(self.get_config_from_env())
        self.config.update(self.get_config_from_cl())
