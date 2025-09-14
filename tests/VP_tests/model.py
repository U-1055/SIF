import json
import random

from src.gui.interfaces import Model, ConfigStruct
from pathlib import Path
import src.gui.gui_const as const


class TestModel(Model):
    """The test stub of Model."""

    def __init__(self, path: Path, config_example: ConfigStruct):
        super().__init__(path, config_example)

        self._is_log = False
        self._config_name = self._get_last_config_name()

    def _get_last_config_name(self):
        configs = tuple(config.name for config in self._path.iterdir())
        return configs[2]

    def _get_full_config(self, config_name: str) -> ConfigStruct:
        with open(Path(self._path, config_name), 'r') as config_file:
            return json.load(config_file)

    def get_config(self, config_name: str, filter_num: int) -> ConfigStruct:
        """Возвращает текущий конфиг с фильтром по заданному номеру."""
        config = self._get_full_config(config_name)
        config[const.FILTERS] = [config[const.FILTERS][filter_num]]
        return config

    def save_config(self, config_name: str, filter_num: int, config: ConfigStruct):
        """Сохраняет конфиг под заданным именем."""
        full_config = self._get_full_config(config_name)
        full_config[const.FILTERS][filter_num] = config[const.FILTERS][0]

        with open(Path(self._path, config_name), 'w') as config_file:
            json.dump(full_config, config_file)

    def add_config(self, config_name: str):
        with open(Path(self._path, config_name), 'w') as config_file:
            json.dump(self._config_example, config_file)

    def add_filters(self, config_name: str):
        with open(Path(self._path, config_name)) as config_file:
            config: ConfigStruct = json.load(config_file)

        config[const.FILTERS].append(self._config_example[const.FILTERS][0])

        with open(Path(self._path, config_name), 'w') as config_file:
            json.dump(config, config_file)

    def get_config_data(self):
        configs = tuple(config.name for config in self._path.iterdir())
        with open(Path(self._path, configs[2])) as config_file:
            config = json.load(config_file)

        return {
            const.CONFIG_NAME: configs[2],
            const.FILTERS: len(config[const.FILTERS]),
            const.CONFIGS_LIST: configs
        }

    @property
    def config_name(self) -> str:
        return self._config_name

    def get_style(self, style_name: str) -> str:
        style_path = r"C:\Users\filat\PycharmProjects\NNFCV\data\gui_data\styles\light_theme.qss"
        if Path(style_path).is_file():
            with open(style_path) as style:
                return style.read()
