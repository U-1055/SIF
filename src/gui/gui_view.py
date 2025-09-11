from PySide6.QtWidgets import (QMainWindow, QWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLineEdit, QFormLayout, QIntList, QLabel, QTextEdit, QComboBox, QLayout)
from PySide6.QtCore import Qt

import typing as tp

from interfaces import Presenter, View, ConfigStruct, ViewConfigStruct
import gui_const as const
import gui_widgets as inp


class MainWindow(QMainWindow, View):
    """
    Основное окно.
    """
    #  константы ключей словаря
    INPUT_PARAMS = 3
    INPUT_DIR = 'input_dir'
    TOTAL_IMAGES = 'total_images'
    THREADS = 'threads'

    FILTERS = 'filters'
    FORMAT = 'format'
    WEIGHT = 'weight'
    EXTENSION = 'extension'
    NUMBER_MULTIPLICITY = 'number_multiplicity'
    CONTENT = 'content'
    PREPARED = 'prepared'

    ACTIONS = 'actions'
    RESIZE = 'resize'
    CROP = 'crop'
    REFORMAT = 'reformat'
    SAVE = 'save'
    DELETE = 'delete'
    OUTPUT_DIR = 'output_dir'

    def __init__(self, presenter: Presenter = None):
        super().__init__(presenter)
        if presenter:
            self.set_presenter(presenter)
        else:
            self._config_struct: ViewConfigStruct | None = None
            self._config_data: dict | None = None
        self._wdg_data: dict[str, QWidget | QFormLayout | QLayout | inp.InputWidget | QComboBox] = {}
        self._base_initialize()

    def _base_initialize(self):
        self._main_layout = QVBoxLayout()
        self._wdg_data[self.MAIN] = self._main_layout

        container = QWidget()
        container.setLayout(self._main_layout)
        self.setCentralWidget(container)

    def _place_widgets(self):
        main_layout = QVBoxLayout()
        control_layout = QHBoxLayout()
        tools_layout = QHBoxLayout()
        form_layout = QGridLayout()
        self._settings_layout = QFormLayout()
        self._filters_layout = QFormLayout()
        self._actions_layout = QFormLayout()

        wdg_switch_config = QComboBox()
        wdg_switch_config.addItems(self._config_list)

        self._settings_layout.addWidget(wdg_switch_config)

        form_layout.addLayout(self._settings_layout, 0, 0, 1, 2)
        form_layout.addLayout(self._filters_layout, 1, 0)
        form_layout.addLayout(self._actions_layout, 1, 1)

        self._place_form()
        self._place_filters()

        container = QWidget()

        self._wdg_error = QLabel()
        self._btn_start = QPushButton(const.START)
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

    def _place_form(self):
        """Размещает форму."""
        wdg_input_dir = inp.QInpLineEdit()
        wdg_input_dir.add_to_struct(self._config_struct, self.INPUT_DIR)

        wdg_threads = inp.QInpSpinBox()
        wdg_threads.add_to_struct(self._config_struct, self.THREADS)
        wdg_threads.setMaximum(12)

        wdg_total_images = inp.QInpSpinBox()
        wdg_total_images.add_to_struct(self._config_struct, self.TOTAL_IMAGES)
        wdg_total_images.setMaximum(32768)
        wdg_total_images.setAccelerated(True)

        wdg_switch_filters = QComboBox()
        wdg_switch_filters.addItems([str(i) for i in range(1, self._filters_num + 1)])
        wdg_switch_filters.activated.connect(self._change_filters)

        self._settings_layout.addWidget(wdg_input_dir)
        self._settings_layout.addWidget(wdg_threads)
        self._settings_layout.addWidget(wdg_total_images)
        self._settings_layout.addWidget(wdg_switch_filters)

    def _place_filters(self):

        wdg_format = inp.QInpComboBox(self._formats)
        wdg_format.add_to_struct(self._config_struct[self.FILTERS][0], self.FORMAT)

        wdg_weight = inp.QInpSpinBox()
        wdg_weight.add_to_struct(self._config_struct[self.FILTERS][0], self.WEIGHT)

        wdg_ext = inp.QInpComboBox(self._formats)
        wdg_ext.add_to_struct(self._config_struct[self.FILTERS][0], self.EXTENSION)

        wdg_num_multiplicity = inp.QInpSpinBox()
        wdg_num_multiplicity.add_to_struct(self._config_struct[self.FILTERS][0], self.NUMBER_MULTIPLICITY)

        wdg_content = inp.QInpLineEdit()
        wdg_content.add_to_struct(self._config_struct[self.FILTERS][0], self.CONTENT)

        wdg_prepared = inp.QInpSpinBox()
        wdg_prepared.add_to_struct(self._config_struct[self.FILTERS][0], self.PREPARED)

        wdg_resize = inp.QInpIntFields(2)
        wdg_resize.add_to_struct(self._config_struct[self.FILTERS][0][self.ACTIONS], self.RESIZE)

        wdg_crop = inp.QInpIntFields(4)
        wdg_crop.add_to_struct(self._config_struct[self.FILTERS][0][self.ACTIONS], self.CROP)

        wdg_reformat = inp.QInpComboBox(self._formats)
        wdg_reformat.add_to_struct(self._config_struct[self.FILTERS][0][self.ACTIONS], self.REFORMAT)

        wdg_save = inp.QInpCheckBox()
        wdg_save.add_to_struct(self._config_struct[self.FILTERS][0][self.ACTIONS], self.SAVE)

        wdg_delete = inp.QInpCheckBox()
        wdg_delete.add_to_struct(self._config_struct[self.FILTERS][0][self.ACTIONS], self.DELETE)

        wdg_output_dir = inp.QInpPathEdit()
        wdg_output_dir.add_to_struct(self._config_struct[self.FILTERS][0][self.ACTIONS], self.OUTPUT_DIR)

        for wdg in ((wdg_format, const.TEXT_FORMAT), (wdg_weight, const.TEXT_WEIGHT), (wdg_ext, const.TEXT_EXTENSION),
                    (wdg_num_multiplicity, const.TEXT_NUMBER_MULTIPLICITY), (wdg_content, const.TEXT_CONTENT), (wdg_prepared, const.TEXT_PREPARED)):
            self._filters_layout.addRow(wdg[1], wdg[0])

        for wdg in ((wdg_resize, const.TEXT_RESIZE), (wdg_crop, const.TEXT_CROP), (wdg_reformat, const.TEXT_REFORMAT),
                    (wdg_save, const.TEXT_SAVE), (wdg_delete, const.TEXT_DELETE), (wdg_output_dir, const.TEXT_OUTPUT_DIR)):
            self._actions_layout.addRow(wdg[1], wdg[0])

    def _change_filters(self, new_filter: int):
        self._presenter.change_filters(new_filter)

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
        self.update_config()

    def update_config(self):
        pass

    def widget_state(self):
        pass

    def show_error(self, widgets: tp.Collection[str], error_text: str):
        for widget in widgets:
            self._config_struct[widget].to_error()

    def show_msg(self, msg: str):
        self._wdg_show_reports.insertPlainText(msg)

    def change_theme(self, style):
        pass

    def insert_text(self, widget: str, text: str):
        self._wdg_data[widget].insert_data(text)

    def clear(self, widget: str):
        self._wdg_data[widget].clear_widget()

    def get_text(self, widget: str):
        self._wdg_data[widget]: inp.InputWidget
        self._wdg_data[widget].get()

    def _add_widget(self, key: str, widget: QWidget, label: str, field: str, tooltip: str | None = None):
        if tooltip:
            widget.setToolTip(tooltip)
        self._wdg_data[key] = widget
        self._wdg_data[field].addRow(label, widget)

    def add_field(self, key: str, label: str | None, field: str | None, tooltip: str | None = None):
        wdg = QFormLayout()
        if field:
            self._wdg_data[field].addLayout(wdg)
        self._wdg_data[key] = wdg

    def add_combobox(self, key: str, label: str, field: str, values: tp.Sequence[str], tooltip: str | None = None):
        self._add_widget(key, inp.QInpComboBox(values), label, field, tooltip)

    def add_path_edit(self, key: str, label: str, field: str, tooltip: str | None = None):
        self._add_widget(key, inp.QInpPathEdit(), label, field, tooltip)

    def add_counter(self, key: str, label: str, field: str, min_: int, max_: int, tooltip: str | None = None):
        self._add_widget(key, inp.QInpSpinBox(min_, max_), label, field, tooltip)

    def add_wdg_many_fields(self, key: str, label: str, field: str, fields: int, min_: int, max_: int, tooltip: str | None = None):
        self._add_widget(key, inp.QInpIntFields(fields, min_, max_), label, field, tooltip)

    def add_memory_counter(self, key: str, label: str, field: str, tooltip: str | None = None):
        self._add_widget(key, inp.QInpMemoryEditComboBox(), label, field, tooltip)

    def add_line_edit(self, key: str, label: str, field: str, tooltip: str | None = None):
        self._add_widget(key, inp.QInpLineEdit(), label, field, tooltip)

    def add_control_btn(self, key: str, label: str, field: str, command: tp.Callable, tooltip: str | None = None):
        btn_control = QPushButton(label)
        btn_control.clicked.connect(command)
        if tooltip:
            btn_control.setToolTip(tooltip)
        self._wdg_data[key] = btn_control
        self._wdg_data[field].addWidget(btn_control)

    def add_control_combobox(self, key: str, field: str, command: tp.Callable, values: tuple | list, tooltip: str | None = None):
        control_cbox = inp.QInpComboBox(values)
        control_cbox.currentIndexChanged.connect(command)

        self._wdg_data[key] = control_cbox
        self._wdg_data[field].addWidget(control_cbox)

    def add_switch(self, key: str, label: str, field: str, state: bool, tooltip: str | None = None):
        self._add_widget(key, inp.QInpCheckBox(state), label, field)

    def add_text_shower(self, key: str, label: str, field: str, tooltip: str | None = None):
        pass

    def insert_control_combobox(self, key: str, insert: str):
        combobox: QComboBox = self._wdg_data[key]
        if insert not in tuple(combobox.itemText(idx) for idx in range(combobox.count())):
            combobox.addItem(insert)
        combobox.setCurrentText(insert)

    @tp.overload
    def insert(self, widget: str, input_: str): pass
    def insert(self, widget: str, input_: tuple):
        self._wdg_data[widget].insert_data(input_)

    @tp.overload
    def get(self, widget: str) -> str: pass
    def get(self, widget: str) -> tuple:
        return self._wdg_data[widget].get()
