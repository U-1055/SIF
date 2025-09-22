import enum
import pathlib
from abc import abstractmethod, abstractproperty

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
                                 'delete': False,
                                 'output_dir': ''
                                }
                          }
                         ]
}


class View:

    MAIN = 'main_field'

    def __init__(self, presenter: 'Presenter' = None):
        if presenter:
            self._presenter: Presenter | None = presenter
        else:
            self._presenter: Presenter | None = None

    @abstractmethod
    def update_form(self, config: ConfigStruct):
        pass

    @abstractmethod
    def bind_widgets(self, widgets: tuple[str], binding: str):
        pass

    @abstractmethod
    def add_field(self, key: str, label: str | None, field: str, type_: str = 'v', tooltip: str | None = None):
        """
        Add field named key to field.
        :param key: adding field's name.
        :param label: label on the field.
        :param field: parent field.
        :param type_: type of the field. Must be "v" - vertical, "h" - horizontal or "f" - form.
        :param tooltip: tooltip of the field.
        """

    @abstractmethod
    def add_line_edit(self, key: str, label: str, field: str, alignment: tp.Any, tooltip: str | None = None):
        pass

    @abstractmethod
    def add_counter(self, key: str, label: str, field: str, min_: int, max_: int, alignment: tp.Any, tooltip: str | None = None):
        pass

    @abstractmethod
    def add_form_switch(self, key: str, label: str, field: str, alignment: tp.Any, tooltip: str | None = None):
        pass

    @abstractmethod
    def add_combobox(self, key: str, label: str, field: str, values: tp.Sequence[str], alignment: tp.Any, tooltip: str | None = None):
        pass

    @abstractmethod
    def add_switch_counter(self, key: str, label: str, field: str, units: tp.Sequence, alignment: tp.Any, tooltip: str | None = None):
        pass

    @abstractmethod
    def add_memory_counter(self, key: str, label: str, field: str, alignment: tp.Any, tooltip: str | None = None):
        pass

    @abstractmethod
    def add_wdg_many_fields(self, key: str, label: str, field: str, fields: int, min_: int, max_: int, alignment: tp.Any, tooltip: str | None = None):
        pass

    @abstractmethod
    def add_wdg_resolution_edit(self, key: str, label: str, field: str, min_: int, max_: int, alignment: tp.Any, tooltip: str | None = None):
        pass

    @abstractmethod
    def add_switch(self, key: str, label: str, field: str, state: bool, alignment: tp.Any, tooltip: str | None = None):
        pass

    @abstractmethod
    def add_path_edit(self, key: str, label: str, field: str, alignment: tp.Any, tooltip: str | None = None):
        pass

    # ToDo: продукоментировать по окончании работы

    @abstractmethod
    def add_text_shower(self, key: str, label: str, field: str, alignment: tp.Any, tooltip: str | None = None):
        pass

    @abstractmethod
    def add_button(self, field: str, alignment: tp.Any, tooltip: str | None = None):
        pass

    @abstractmethod
    def add_control_btn(self, key: str, label: str, field: str, command: tp.Callable, alignment: tp.Any, tooltip: str | None = None):
        pass

    @abstractmethod
    def add_control_combobox(self, key: str, field: str, command: tp.Callable, values: tuple | list, alignment: tp.Any, tooltip: str | None = None):
        """
        ...
        :param command: a callable object that has 1 argument of type int
                        (to that will send index of item what was chosen by user).
        """

    @abstractmethod
    def add_label(self, key: str, text: str, field: str, alignment: tp.Any):
        pass

    @abstractmethod
    def show_input_dialog_window(self, title: str, message: str = None) -> ...:
        pass

    @abstractmethod
    def insert_control_combobox(self, key: str, insert: str):
        pass

    @tp.overload
    @abstractmethod
    def insert(self, widget: str, input_: str): pass
    def insert(self, widget: str, input_: tuple): pass

    @tp.overload
    @abstractmethod
    def get(self, widget: str) -> str: pass
    def get(self, widget: str) -> tuple: pass

    def clear(self, widget: str):
        pass

    @abstractmethod
    def show_errors(self, widgets: tp.Collection[str]):
        pass

    @abstractmethod
    def apply_main_style(self, style: str):
        pass

    @abstractmethod
    def apply_style(self, widget: str, style: str):
        pass

    def set_presenter(self, presenter: 'Presenter' = None):
        self._presenter = presenter

    def show_msg(self, msg: str):
        """Show message in widget"""

    def update_config(self):
        """Обновляет конфиг"""

    @property
    def root_field(self):
        """Return the name of the root field ("main_field" default)."""
        return self.MAIN

    @property
    @abstractmethod
    def alignment_right(self):
        """Returns value of right alignment flag for this View."""
        pass

    @property
    @abstractmethod
    def alignment_left(self):
        """Returns value of left alignment flag for this View."""
        pass

    @property
    @abstractmethod
    def alignment_top(self):
        """Returns value of top alignment flag for this View."""
        pass

    @property
    @abstractmethod
    def alignment_bottom(self):
        """Returns value of bottom alignment flag for this View."""
        pass


class Model:

    def __init__(self, path: pathlib.Path, config_example: ConfigStruct, filters: str, actions: str, style_table: dict):
        self._is_log: bool = False
        self._config_name: str = self._get_config_name()
        self._config_example = config_example
        self._path = path

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
    def add_config(self, config_name: str):
        pass

    @abstractmethod
    def add_filters(self, config_name: str):
        pass

    @abstractmethod
    def get_config_data(self) :
        """
        Возвращает информацию о конфигах в виде:
        {config_name: "Имя последнего конфига",
         config_list: "Имена всех конфигов",
         "filters": число фильтров в последнем конфиге}
        """

    @abstractmethod
    def get_style(self, style_name: str) -> str:
        """Возвращает строку стиля QSS."""

    @abstractmethod
    def change_style(self, style_name):
        """Writes last style's name to the info file."""
        pass

    @property
    @abstractmethod
    def current_style(self) -> str:
        pass

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
    def __init__(self, validation_params: dict, styles_table: tuple, elements: enum.Enum, model=None, view=None):
        """
        Initialize an instance of the class.

        :param validation_params: the parameters that will use for validation.
        :param styles_table: the dict with keys that means style's name and values that means a QSS-file that contains this style.
        :param elements: elements of the GUI.
        :param model: Model's instance.
        :param view: View's instance.
        """
        self._model: Model = model
        self._view: View = view
        self._config_struct: ConfigStruct = config
        self._filters_now: int = 0

    @abstractmethod
    def prepare_data(self):
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


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

    app = QApplication()

    root = QMainWindow()
    wdg = QWidget()

    root.setCentralWidget(wdg)
    root.setMinimumSize(150, 150)
    root.show()

    app.exec()
