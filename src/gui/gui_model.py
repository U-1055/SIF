from pathlib import Path

from interfaces import Model, ConfigStruct, Filter
import gui_const as const


class Saver(Model):

    def __init__(self):
        super().__init__()
        self._path: Path

    def _load_last_data(self):
        pass

    def get_config(self, config_name: str, filter_num: int) -> ConfigStruct:
        """Возвращает текущий конфиг."""

    def save_config(self, config_name: str, filter_num: int, config: ConfigStruct):
        """Сохраняет конфиг под заданным именем."""

    def add_filter(self, config_name: str, filter_: Filter):
        pass

    def get_config_data(self):
        return {
            const.CONFIG_NAME: 'Stub_config',
            const.FILTERS: 2,
            const.CONFIGS_LIST: ('Stub_config', 'sth', 'sth2')
            }

    def config_name(self) -> str:
        pass

