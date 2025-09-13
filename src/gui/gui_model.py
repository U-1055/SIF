from pathlib import Path

from interfaces import Model, ConfigStruct, Filter
import gui_const as const


class Saver(Model):

    def __init__(self, path: Path):
        super().__init__()
        self._path: path

    def _load_last_data(self):
        pass

    def _get_full_config(self):
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

    def get_style(self, style_name: str) -> str:
        if Path(style_name).is_file():
            with open(Path(self._path, f'{style_name}.qss')) as style:
                return style.read()

