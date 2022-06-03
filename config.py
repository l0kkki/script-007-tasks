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
             - log_dir
             - log_level
        """

        parser = argparse.ArgumentParser()
        parser.add_argument('-d',
                            '--directory',
                            help='Path to working directory')
        parser.add_argument('--log_dir',
                            help='Path to logging directory')
        parser.add_argument('--log_level',
                            choices=[10, 20, 30, 40, 50],
                            type=int,
                            help='Logging level')
        cmd_params = parser.parse_args().__dict__
        return {key: value for key, value in cmd_params.items() if value is not None}

    @staticmethod
    def get_config_from_env():
        """ Get application params from Environment arguments

        Returns:
            Dict with non empty value:
             - directory
             - log_dir
             - log_level
        """

        accord_dict = {
            'FILE_SERVER_DIRECTORY': 'directory',
            'FILE_SERVER_LOG_DIR': 'log_dir',
            'FILE_SERVER_LOG_LEVEL': 'log_level'
        }
        return {accord_dict[key]: val for key, val in os.environ.items() if key in accord_dict and val is not None}

    @staticmethod
    def get_config_from_file():
        """ Get application params from config.yaml arguments

        Returns:
            Dict with non empty value:
             - directory
             - log_dir
             - log_level
        """
        yaml_conf = {}
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as conf_file:
                yaml_conf = yaml.load(conf_file, Loader=yaml.Loader)
        except Exception as ex:
            with open('CONFIG_WARNING.txt', 'w') as warning_file:
                warning_file.write(f'Cant read config.yaml, catch exception {ex}')
        return yaml_conf

    def __init__(self, main_dir):
        # default config
        self.config = {
            'directory': os.path.join(main_dir, 'FileServer'),
            'log_dir': os.path.join(main_dir, 'Logs'),
            'log_level': 20
        }
        self.config.update(self.get_config_from_file())
        self.config.update(self.get_config_from_env())
        self.config.update(self.get_config_from_cl())
