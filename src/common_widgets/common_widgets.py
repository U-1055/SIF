from PySide6.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QLabel, QSpinBox, QPushButton, QFileDialog, QComboBox
from PySide6.QtGui import QValidator, Qt
from PySide6.QtCore import QObject

import typing as tp

Align = Qt.AlignmentFlag


class QManyField(QWidget):
    """
    Widget with many horizontal fields. Number of fields is passed to the constructor.

    :param fields: number of fields.
    :param separator: string what will separate the fields.
    """

    def __init__(self, fields: int, separator: str = 'x'):
        super().__init__()
        self._widgets: list[QLineEdit | QSpinBox] = []
        self._separators: list[QLabel] = []
        self._fields = fields
        if self._fields < 1:
            raise ValueError(f"Parameter <fields> can't be {self._fields}, must be >= 1")
        self._separator = separator
        self._place_widgets()

    def _place_widgets(self):
        main_layout = QHBoxLayout()
        wdg_field = QLineEdit()
        main_layout.addWidget(wdg_field, Align.AlignLeft)
        self._widgets.append(wdg_field)

        for i in range(self._fields - 1):
            wdg_sep = QLabel(self._separator)
            wdg_field = QLineEdit()

            main_layout.addWidget(wdg_sep, Align.AlignLeft)
            main_layout.addWidget(wdg_field, Align.AlignLeft)
            self._widgets.append(wdg_field)
            self._separators.append(wdg_sep)

        self.setLayout(main_layout)

    def insert(self, idx: int, value: str):
        if idx >= self._fields:
            raise IndexError(f"Widget index must be less than num of the fields ({self._fields}). Your widget index = {idx}")
        self._widgets[idx].insert(value)

    def clear(self, idx: int):
        if idx >= self._fields:
            raise IndexError(f"Widget index must be less than num of the fields ({self._fields}). Your widget index = {idx}")
        self._widgets[idx].clear()

    def value(self, idx: int) -> str:
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


class QManyIntField(QManyField):
    def __init__(self, field: int, separator: str = 'x', min_value: int = 0, max_value: int = 99):
        self._min_value, self._max_value = min_value, max_value
        super().__init__(field, separator)

    def _place_widgets(self):
        main_layout = QHBoxLayout()
        wdg_field = QSpinBox()
        wdg_field.setMinimum(self._min_value)
        wdg_field.setMaximum(self._max_value)
        main_layout.addWidget(wdg_field, Align.AlignLeft)
        self._widgets.append(wdg_field)

        for i in range(self._fields - 1):
            wdg_sep = QLabel(self._separator)
            wdg_field = QSpinBox()
            wdg_field.setMinimum(self._min_value)
            wdg_field.setMaximum(self._max_value)
            main_layout.addWidget(wdg_sep, Align.AlignLeft)
            main_layout.addWidget(wdg_field, Align.AlignLeft)
            self._widgets.append(wdg_field)
            self._separators.append(wdg_sep)

        self.setLayout(main_layout)

    def insert(self, idx: int, value: int):
        if idx >= self._fields:
            raise IndexError(f"Widget index must be less than num of the fields ({self._fields}). Your widget index = {idx}")
        self._widgets[idx].setValue(int(value))

    def value(self, idx: int) -> int:
        if idx >= self._fields:
            raise IndexError(f"Widget index must be less than num of the fields ({self._fields}). Your widget index = {idx}")
        return self._widgets[idx].value()


class QPathEdit(QWidget):
    """
    QLineEdit with button what open QFileDialog, where a user may choose a file.
    """
    def __init__(self, placeholder_text: str = '', btn_text: str = '...', is_dir: bool = False, is_file: bool = True):
        super().__init__()
        if not is_dir and not is_file:
            raise ValueError('Params is_dir and is_file cannot be False at the same time.')
        self._is_dir, self._is_file = is_dir, is_file
        self._placeholder = placeholder_text
        self._btn_text = btn_text
        self._place_widgets()  # ToDo: сделать тестовую среду для виджетов

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
        if self._is_dir:
            path = filedialog.getExistingDirectoryUrl()
        else:
            path = filedialog.getOpenFileUrl()
        self._main_edit.insert(path[0].path())

    def insert(self, text: str):
        self._main_edit.insert(text)

    def clear(self):
        self._main_edit.clear()

    def text(self):
        return self._main_edit.text()


class QLineEditComboBox(QWidget):
    """
    The QComboBox and QWidget what supporting user's input. You can get tuple of the QLineEdit's value and the
    QComboBox's value.

    :param field: subclass of QWidget. It using as a field.
    :param values: values for QComboBox.
    """

    def __init__(self, field=QLineEdit, values: tp.Sequence[str] = ()):
        super().__init__()
        self._values = values
        self._field = field
        self._place_widgets()

    def _place_widgets(self):
        main_layout = QHBoxLayout()

        self._wdg_edit = self._field()
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

    def insert(self, text: str, value: str):
        if value not in self._values:
            raise ValueError(f'Unknown value {value}. Value must be contained in values of this widget.')
        self._wdg_edit.insert(text)
        self._wdg_combobox.setCurrentText(value)

    def clear(self):
        if len(self._values) > 0:
            self._wdg_combobox.setCurrentIndex(0)
        self._wdg_edit.clear()


