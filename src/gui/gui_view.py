from PySide6.QtWidgets import (QMainWindow, QWidget, QPushButton, QVBoxLayout, QFormLayout, QComboBox, QLayout, QInputDialog,
                               QHBoxLayout, QTextEdit, QLabel, QFrame, QDialog)
from PySide6.QtGui import Qt
import typing as tp

from interfaces import Presenter, View
import gui_widgets as inp

Align = Qt.AlignmentFlag


class MainWindow(QMainWindow, View):
    """
    Основное окно.
    """

    def __init__(self, presenter: Presenter = None, event_callback: tp.Callable = lambda: None):
        super().__init__(presenter)
        if presenter:
            self.set_presenter(presenter)
        self._wdg_data: dict[str, QWidget | QFormLayout | QVBoxLayout | QHBoxLayout | inp.InputWidget | QComboBox] = {}
        self._event_callback = event_callback
        self._base_initialize()

    def _base_initialize(self):
        self._main_layout = QVBoxLayout()
        self._wdg_data[self.MAIN] = self._main_layout

        container = QWidget()
        container.setLayout(self._main_layout)
        self.setCentralWidget(container)

    def _cancel_error(self):
        """Переводит виджеты из состояния ошибки в нормальное состояние"""
        pass

    def set_presenter(self, presenter: 'Presenter' = None):
        self._presenter = presenter
        self.update_config()

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

    def _add_widget(self, key: str, widget: QWidget, label: str, field: str, alignment: Align, tooltip: str | None = None):
        if tooltip:
            widget.setToolTip(tooltip)
        self._wdg_data[key] = widget
        if isinstance(self._wdg_data[field], QFormLayout):
            self._wdg_data[field].addRow(label, widget)
        else:
            self._wdg_data[field].addWidget(widget, alignment=Align.AlignLeft)

    def add_field(self, key: str, label: str | None, field: str, type_: str = 'v', tooltip: str | None = None):
        match type_:
            case 'v':
                wdg = QVBoxLayout()
            case 'h':
                wdg = QHBoxLayout()
            case 'f':
                wdg = QFormLayout()
            case _:
                raise ValueError(f'Unknown type of field: {type_}')

        self._wdg_data[field].addLayout(wdg)
        self._wdg_data[key] = wdg

    def add_combobox(self, key: str, label: str, field: str, values: tp.Sequence[str], alignment: Align, tooltip: str | None = None):
        self._add_widget(key, inp.QInpComboBox(values), label, field, alignment, tooltip)

    def add_path_edit(self, key: str, label: str, field: str, alignment: Align, tooltip: str | None = None):
        self._add_widget(key, inp.QInpPathEdit(), label, field, alignment, tooltip)

    def add_counter(self, key: str, label: str, field: str, min_: int, max_: int, alignment: Align, tooltip: str | None = None):
        self._add_widget(key, inp.QInpSpinBox(min_, max_), label, field, alignment, tooltip)

    def add_wdg_many_fields(self, key: str, label: str, field: str, fields: int, min_: int, max_: int, alignment: Align, tooltip: str | None = None):
        self._add_widget(key, inp.QInpIntFields(fields, min_, max_), label, field, alignment, tooltip)

    def add_wdg_resolution_edit(self, key: str, label: str, field: str, min_: int, max_: int, alignment: tp.Any, tooltip: str | None = None):
        self._add_widget(key, inp.QInpResolutionEdit(min_, max_), label, field, alignment, tooltip)

    def add_memory_counter(self, key: str, label: str, field: str, alignment: Align, tooltip: str | None = None):
        self._add_widget(key, inp.QInpWeightEdit(), label, field, alignment, tooltip)

    def add_line_edit(self, key: str, label: str, field: str, alignment: Align, tooltip: str | None = None):
        self._add_widget(key, inp.QInpLineEdit(), label, field, alignment, tooltip)

    def add_control_btn(self, key: str, label: str, field: str, command: tp.Callable, alignment: Align = Align.AlignCenter, tooltip: str | None = None):
        btn_control = QPushButton(label)
        btn_control.clicked.connect(command)
        if tooltip:
            btn_control.setToolTip(tooltip)
        self._wdg_data[key] = btn_control
        self._wdg_data[field].addWidget(btn_control)

    def add_control_combobox(self, key: str, field: str, command: tp.Callable, values: tuple | list, alignment: Align, tooltip: str | None = None):
        control_cbox = inp.QInpComboBox(values)
        control_cbox.currentIndexChanged.connect(command)

        if tooltip:
            control_cbox.setToolTip(tooltip)

        self._wdg_data[key] = control_cbox
        self._wdg_data[field].addWidget(control_cbox)

    def add_switch(self, key: str, label: str, field: str, state: bool, alignment: Align, tooltip: str | None = None):
        self._add_widget(key, inp.QInpCheckBox(state), label, field, alignment, tooltip)

    def add_text_shower(self, key: str, label: str, field: str, alignment: Align, tooltip: str | None = None):
        wdg_text = QTextEdit()
        self._wdg_data[key] = wdg_text  # ToDo: добавить метод для обновления словаря без замены существующего ключа (кидать исключение при наличии ключа в словаре)
        self._wdg_data[field].addWidget(wdg_text)

    def show_input_dialog_window(self, title: str, message: str = None) -> str:
        win_dialog = QInputDialog()
        frm_temp = QWidget()

        if message is None:
            message = ''
        return win_dialog.getText(frm_temp, title, message)[0]

    def show_control_dialog_window(self, title: str, message: str = None, command: tp.Callable = None):
        win_dialog = QDialog()
        win_dialog.setWindowTitle(title)

        win_dialog.show()
        if command:
            win_dialog.accepted.connect(command)

    def add_label(self, key: str, text: str, field: str, alignment: Align):
        lbl = QLabel(text)
        self._wdg_data[key] = lbl
        self._wdg_data[field].addWidget(lbl, alignment=Align.AlignRight)

    def insert_control_combobox(self, key: str, insert: str):
        combobox: QComboBox = self._wdg_data[key]
        if insert not in tuple(combobox.itemText(idx) for idx in range(combobox.count())):
            combobox.addItem(insert)
            combobox.setCurrentIndex(combobox.count() - 1)

    @tp.overload
    def insert(self, widget: str, input_: str): pass
    def insert(self, widget: str, input_: tuple):
        self._wdg_data[widget].insert_data(input_)

    @tp.overload
    def get(self, widget: str) -> str: pass
    def get(self, widget: str) -> tuple:
        return self._wdg_data[widget].get()

    def apply_style(self, widget: str, style: str):
        self._wdg_data[widget].setStyleSheet(style)

    def apply_main_style(self, style: str):
        self.setStyleSheet(style)

    @property
    def alignment_left(self):
        return Align.AlignLeft

    @property
    def alignment_right(self):
        return Align.AlignRight

    @property
    def alignment_top(self):
        return Align.AlignTop

    @property
    def alignment_bottom(self):
        return Align.AlignBottom
