from pathlib import Path
import shelve as shv
import json

from interfaces import Model, ConfigStruct, Filter
import gui_const as const


class Saver(Model):

    def __init__(self, path: Path, config_example: ConfigStruct, filters: str, actions: str, style_table: dict):
        super().__init__(path, config_example, filters, actions, style_table)
        self._config_example = config_example

        self._path: path
        self._info = 'info.json'
        self._main_data = 'main_data'
        self._configs = 'configs'
        self._gui_data = 'gui_data'
        self._styles = 'styles'
        self._last_style = 'last_style'
        self._last_config = 'last_config'
        self._icons = 'icons'

        self._configs_path: Path = Path(self._path, self._main_data, self._configs)
        self._info_path: Path = Path(self._path, self._main_data, self._info)
        self._styles_path: Path = Path(self._path, self._gui_data, self._styles)
        self._icons_path: Path = Path(self._path, self._gui_data, self._icons)

        self._filters, self._actions = filters, actions
        self._style_table = style_table

    def _restore_info_file(self):
        if self._info_path.is_file():
            with open(self._info_path) as info:
                json.dump(
                    {
                    self._last_config: '',
                    self._last_style: '',
                    self._filters: ''
                },
                info)

    def _update_info(self):
        pass

    def _get_last_config_name(self):
        with open(Path(self._path, self._main_data, self._info), 'rb') as file:
            config_data = json.load(file)

        with shv.open(str(self._configs_path), 'r') as configs:
            if config_data[self._last_config] in configs:
                return config_data[self._last_config]
            else:
                return list(configs.keys())[0]

    def get_full_config(self, config_name: str) -> ConfigStruct:
        with shv.open(str(self._configs_path)) as configs:
            if config_name in configs:
                return configs[config_name]

    def _set_current_config(self, config_name: str):
        """Set the name of the last config."""
        with open(self._info_path) as info:
            info_data = json.load(info)
        with shv.open(str(self._configs_path), 'r') as configs:
            if config_name in configs:
                info_data[self._last_config] = config_name

    def change_style(self, style_name: str):
        with open(self._info_path, 'rb') as info:
            info_data = json.load(info)
        info_data[self._last_style] = style_name
        with open(self._info_path, 'w') as info:
            json.dump(info_data, info)

    def get_config(self, config_name: str, filter_num: int) -> ConfigStruct:
        """Returns the config by given name with filter by given number."""
        config = self.get_full_config(config_name)
        config[self._filters] = [config[self._filters][filter_num]]
        return config

    def save_config(self, config_name: str, filter_num: int, config: ConfigStruct):
        """Сохраняет конфиг под заданным именем."""
        full_config = self.get_full_config(config_name)
        full_config[self._filters][filter_num] = config[self._filters][0]

        for key in full_config:
            if key in config and key != const.FILTERS:
                full_config[key] = config[key]

        with shv.open(str(self._configs_path), 'w') as configs:
            configs[config_name] = full_config

    def add_config(self, config_name: str):
        with shv.open(str(self._configs_path), 'w') as config_file:
            config_file[config_name] = self._config_example

    def add_filters(self, config_name: str):
        with shv.open(str(self._configs_path), 'r') as configs:
            config = configs[config_name]
            config[self._filters].append(self._config_example[self._filters][0])

        with shv.open(str(self._configs_path), 'w') as configs:
            configs[config_name] = config

    def del_config(self, config_name: str):
        with shv.open(str(self._configs_path), 'w') as configs:
            configs.pop(config_name)

        with open(self._info_path) as info:
            info_data = json.load(info)
        if info_data[self._last_config] == config_name:
            info_data[self._last_config] = ''

        with open(self._info_path, 'w') as info:
            json.dump(info_data, info)

    def get_config_data(self):
        with shv.open(str(self._configs_path), 'r') as configs:
            last_config_name = self._get_last_config_name()

            return {
                const.CONFIG_NAME: last_config_name,
                self._filters: len(configs[last_config_name][self._filters]),
                const.CONFIGS_LIST: tuple(configs.keys())
            }

    @property
    def config_name(self) -> str:
        return self._get_last_config_name()

    @property
    def current_style(self) -> str:
        with open(self._info_path) as info:
            return json.load(info)[self._last_style]

    def get_style(self, style_name: str) -> str:
        style_path = Path(self._styles_path, self._style_table[style_name])
        if Path(style_path).is_file():
            with open(style_path) as style_file:
                style = style_file.read()
            with open(self._info_path, 'rb') as info:
                info_data = json.load(info)
                info_data[self._last_style] = style_name
            return style


if __name__ == '__main__':
    from PySide6.QtWidgets import QMainWindow, QApplication

    from interfaces import config
    from tests.common_tests.save_load_test import ModelTest
    from gui_presenter import LogicManager
    from gui import init_view
    import gui_const as const

    cases_path = Path('..', '..', 'data', 'test_data', 'cases', 'model_cases')
    root = ModelTest(cases_path)
    path = Path('..', '..', 'data')

    model = Saver(path, config, 'filters', 'actions', const.styles)

    presenter = LogicManager({}, const.styles, const.Elements, const.labels, const.tooltips, model, root)
    root.set_presenter(presenter)

    test_config = root.get_test_case(0)
    root.insert_config(test_config)

    root_config = root.get_config()
    root.check_config(0, root_config)

