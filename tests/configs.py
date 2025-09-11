import json
import test_data as td
from pathlib import Path

def create_configs(num: int):
    config = {
                   'input_dir': '', 'total_images': '', 'threads': 1,
                   'filters': #-----------------------------------------------------------------------------------------
                         [
                          {
                            'format': '',
                            'size': '',
                            'weight': '',
                            'name': '',
                            'extension': '',
                            'number_multiplicity': '',
                            'content': '',
                            'prepared': '',
                            'actions':  # -----------------------------------------------------------------------------------
                                {
                                 'resize': '',
                                 'crop': '',
                                 'reformat': '',
                                 'rename': '',
                                 'save': True,
                                 'delete': True,
                                 'output_dir': ''
                                }
                          }
                         ]
                   }

    with open(Path(td.test_path, 'configs'), 'wb') as config_file:
        json.dump(config_file, config)

if __name__ == '__main__':
    create_configs(1)