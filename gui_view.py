from PySide6.QtWidgets import (QMainWindow, QWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLineEdit, QFormLayout, QIntList, QLabel, QTextEdit, QComboBox)
from PySide6.QtCore import Qt

import typing as tp

from interfaces import Presenter, View, ConfigStruct, ViewConfigStruct
from gui_const import START
import gui_widgets as inp

class MainWindow(QMainWindow, View):
    """
    Основное окно.
    :param start_preparing_method: метод Presenter'а для начала обработки, принимающий входные данные
    :param save_params_method: метод Presenter'а для сохранения текущих настроек обработки
    """
    #  константы ключей словаря
    INPUT_PARAMS = 3
    INPUT_DIR = 'input_dir'
    TOTAL_IMAGES = 'total_images'
    THREADS = 'threads'

    FILTERS = 'filters'
    ACTIONS = 'actions'

    def __init__(self, presenter: Presenter = None):
        super().__init__(presenter)
        if presenter:
            self._config_struct: ViewConfigStruct | None = self._presenter.config_struct
        else:
            self._config_struct: ViewConfigStruct | None = None

    def _place_widgets(self):
        main_layout = QVBoxLayout()
        control_layout = QHBoxLayout()
        tools_layout = QHBoxLayout()
        form_layout = QFormLayout()

        #  размещение виджетов + привязка к конкретному ключу config_struct
        self._place_form(form_layout)

        container = QWidget()

        self._wdg_error = QLabel()
        self._btn_start = QPushButton(START)
        self._wdg_show_reports = QTextEdit()
        self._wdg_show_reports.setReadOnly(True)
        self._wdg_change_filters = QComboBox()

        stub = QWidget()

        main_layout.addLayout(tools_layout, 5)
        main_layout.addLayout(form_layout, 25)
        main_layout.addLayout(control_layout, 15)
        main_layout.addWidget(self._wdg_error, 1)

        control_layout.addWidget(self._btn_start, 1, )
        control_layout.addWidget(self._wdg_show_reports, 4)
        control_layout.addWidget(stub, 5)

        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def _place_form(self, form_layout: QFormLayout):
        """Размещает форму."""
        wdg_input_dir = inp.QInpLineEdit(self._config_struct, self.INPUT_DIR)
        wdg_threads = inp.QInpSpinBox(self._config_struct, self.THREADS)
        wdg_total_images = inp.QInpSpinBox(self._config_struct, self.TOTAL_IMAGES)


        wdg_format = inp.

    def _change_filters(self):
        pass

    def _get_wdg_data(self, widgets: dict) -> dict:
        """
        Получает данные из виджетов переданного словаря, возвращает словарь, в котором виджеты заменены данными из них.
        :param widgets: словарь, по структуре идентичный словарю Presenter'а, содержащий виджеты формы в качестве значений.
        """
        widgets_data = {}
        for key in widgets:
            if key == self.ACTIONS or key == self.FILTERS:
                widgets_data[key] = self._get_wdg_data(widgets[key])
            widgets_data[key] = widgets.get(key)

        return widgets_data

    def _cancel_error(self):
        """Переводит виджеты из состояния ошибки в нормальное состояние"""
        pass

    def _give_data(self):
        """Передаёт данные из виджетов Presenter'у."""
        self._presenter.prepare_data(self._get_wdg_data(self._config_struct))

    def set_presenter(self, presenter: 'Presenter' = None):
        self._presenter = presenter
        self._config_struct = self._presenter.config_struct
        self._place_widgets()

    def widget_state(self):
        pass

    def show_error(self, widgets: tp.Collection[str], error_text: str):
        for widget in widgets:
            self._config_struct[widget].to_error()

    def show_msg(self, msg: str):
        self._wdg_show_reports.insertPlainText(msg)
