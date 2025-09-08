from abc import abstractmethod, abstractproperty
from gui_widgets import InputWidget
import typing as tp

Filter = dict[
    str, str |
    dict[
         str, str | bool]]

ConfigStruct = dict[str, str |  # main dict
                    list[  # filters
                      dict[str, str |  # filter
                           dict[str, str | bool]  # actions
                         ]
                        ]
                   ]

ViewConfigStruct = dict[str, InputWidget |  # main dict
                        list[  # filters
                         dict[str, InputWidget |  # filter
                              dict[str, InputWidget]  # actions
                             ]
                           ]
                       ]

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


class View:

    def __init__(self, presenter: 'Presenter' = None):
        if presenter:
            self._presenter: Presenter | None = presenter
        else:
            self._presenter: Presenter | None = None

    def show_errors(self, widgets: tp.Collection[str]):
        pass

    def set_presenter(self, presenter: 'Presenter' = None):
        self._presenter = presenter

    def show_msg(self, msg: str):
        """Передаёт сообщение в виджет отслеживания обработки."""

    def update_config(self):
        """Обновляет конфиг"""


class Model:

    def __init__(self):
        self._is_log: bool = False
        self._config_name: str = self._get_config_name()

    @abstractmethod
    def _get_config_name(self) -> str:
        pass

    @property
    @abstractmethod
    def config_name(self) -> str:
        return self._config_name

    @abstractmethod
    def get_config(self, config_name: str, filter_num: int) -> ConfigStruct:
        """Возвращает конфиг по заданному имени, содержащий фильтр под заданным номером."""

    @abstractmethod
    def save_config(self, config_name: str, filter_num: int, config_: ConfigStruct):
        """Сохраняет конфиг под заданным именем."""

    @abstractmethod
    def get_config_data(self) :
        """
        Возвращает информацию о конфигах в виде:
        {config_name: "Имя последнего конфига",
         config_list: "Имена всех конфигов",
         "filters": число фильтров в последнем конфиге}
        """

    def create_writing(self):
        """Создаёт новый лог обработки."""
        self._is_log = True

    def write(self):
        """Записывает сообщение в лог обработки (если есть), если его нет - ничего не делает."""
        if self._is_log:
            pass

    def stop_writing(self):
        """Останавливает запись в текущий лог."""
        self._is_log = False


class Presenter:
    def __init__(self, model: Model = None, view: View = None):
        self._model: Model = model
        self._view: View = view
        self._config_struct: ConfigStruct = config
        self._filters_now: int = 0

    @abstractmethod
    def prepare_data(self, data: ConfigStruct):
        """Обрабатывает данные от View."""
        pass

    @property
    def config_struct(self) -> ConfigStruct:
        return self._config_struct

    @property
    @abstractmethod
    def init_data(self) -> dict:
        pass

    def set_model(self, model: Model):
        self._model = model

    def set_view(self, view: View):
        self._view = view

    @abstractmethod
    def change_filters(self, filter_num: int):
        pass
