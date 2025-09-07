from PySide6.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QLabel, QSpinBox, QPushButton, QFileDialog, QComboBox
from PySide6.QtGui import QValidator
from PySide6.QtCore import QObject

import typing as tp


class QManyField(QWidget):
    """
    Widget with many horizontal fields. Number of fields is passed to the constructor.

    :param fields: number of fields.
    :param separator: string what will separate the fields.
    :param field: QWidget class what will use as field. It must have the text() method.
    """

    def __init__(self, fields: int, field, separator: str = 'x'):
        super().__init__()
        self._widgets: list[QLineEdit | QSpinBox] = []
        self._separators: list[QLabel] = []
        self._field = field
        self._fields = fields
        if self._fields < 1:
            raise ValueError(f"Parameter <fields> can't be {self._fields}, must be >= 1")
        self._separator = separator

    def _place_widgets(self):
        main_layout = QHBoxLayout()
        wdg_field = self._field()
        main_layout.addWidget(wdg_field)
        self._widgets.append(wdg_field)

        for i in range(self._fields - 1):
            wdg_sep = QLabel(self._separator)
            wdg_field = self._field()

            main_layout.addWidget(wdg_sep)
            main_layout.addWidget(wdg_field)
            self._widgets.append(wdg_field)
            self._separators.append(wdg_sep)

        self.setLayout(main_layout)

    def insert(self, idx: int, value: str):
        if idx >= self._fields:
            raise IndexError(f"Widget index must be less than num of the fields ({self._fields}). Your widget index = {idx}")
        self._widgets[idx].insert(value)

    def get(self, idx: int) -> str:
        if idx >= self._fields:
            raise IndexError(f"Widget index must be less than num of the fields ({self._fields}). Your widget index = {idx}")
        return self._widgets[idx].text()

    def set_separator(self, separator: str):
        self._separator = separator
        for lbl in self._separators:
            lbl.setText(self._separator)

    def setValidator(self, widget_idx: int, validator: QValidator):
        if widget_idx >= self._fields:
            raise IndexError(f"Widget index must be less than num of the fields ({self._fields}). Your widget index = {widget_idx}")
        self._widgets[widget_idx].setValidator(validator)

    @property
    def widgets(self) -> list[QLineEdit]:
        return self._widgets


class QPathEdit(QWidget):
    """
    QLineEdit with button what open QFileDialog, where a user may choose a file.
    """
    def __init__(self, placeholder_text: str = '', btn_text: str = '...'):
        super().__init__()
        self._placeholder = placeholder_text
        self._btn_text = btn_text
        self._place_widgets()

    def _place_widgets(self):
        main_layout = QHBoxLayout()
        self._main_edit = QLineEdit()
        self._main_edit.setPlaceholderText(self._placeholder)

        btn_filedialog = QPushButton(self._btn_text)
        btn_filedialog.clicked.connect(self._open_filedialog)

        main_layout.addWidget(self._main_edit, 9)
        main_layout.addWidget(btn_filedialog, 1)
        self.setLayout(main_layout)

    def _open_filedialog(self):
        filedialog = QFileDialog()
        path = filedialog.getOpenFileUrl()
        self._main_edit.insert(path[0].path())

    def insert(self, text: str):
        self._main_edit.insert(text)

    def text(self):
        return self._main_edit.text()


class QLineEditComboBox(QWidget):

    def __init__(self, values: tp.Sequence[str]):
        super().__init__()
        self._values = values
    # ToDo: сделать добавление собственного виджета

    def _place_widgets(self):
        main_layout = QHBoxLayout()

        self._wdg_edit = QLineEdit()
        self._wdg_combobox = QComboBox()
        self._wdg_combobox.addItems(self._values)

        main_layout.addWidget(self._wdg_edit, 10)
        main_layout.addWidget(self._wdg_combobox, 1)

        self.setLayout(main_layout)

    def value(self):
        return self._wdg_edit.text(), self._wdg_combobox.currentText()

    @property
    def values(self) -> tp.Sequence:
        return self._values
