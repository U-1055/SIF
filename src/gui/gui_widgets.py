import abc

from PySide6.QtWidgets import QWidget, QLineEdit, QSpinBox, QComboBox, QCheckBox
from abc import abstractmethod
import typing as tp

from src.common_widgets.common_widgets import QManyField, QPathEdit, QLineEditComboBox


class InputWidget:

    @abstractmethod
    def get(self):
        """Возвращает данные из виджета в описанном в нём формате."""

    @abstractmethod
    def to_error(self):
        """Переводит виджет в состояние ошибки."""

    @abstractmethod
    def to_normal(self):
        """Переводит виджет в нормальное состояние."""

    @abstractmethod
    def add_to_struct(self, dict_: dict, key) -> dict:
        """
        Вводит в виджет значение из данного словаря, заменяет введённое значение на экземпляр класса.
        :param dict_: словарь
        :param key: ключ, значение которого должно быть в виджете
        """


class QInpLineEdit(InputWidget, QLineEdit):

    def add_to_struct(self, dict_: dict, key) -> dict:
        self.insert(dict_[key])
        dict_[key] = self
        return dict_

    def get(self):
        return self.text()


class QInpSpinBox(InputWidget, QSpinBox):
    
    def add_to_struct(self, dict_: dict, key) -> dict:
        value = dict_[key]
        if value:
            self.setValue(int(value))

        dict_[key] = self
        return dict_

    def get(self):
        return self.text()


class QInpComboBox(InputWidget, QComboBox):
    
    def __init__(self, values: tp.Iterable):
        super().__init__()
        self._values = values

    def add_to_struct(self, dict_: dict, key) -> dict:
        values = dict_[key]
        if values:
            for idx, value in enumerate(values):
                if value in self._values:
                    self.setCurrentIndex(idx)

        dict_[key] = self
        return dict_

    def get(self):
        return self.currentText()


class QAddCombobox(QComboBox):

    def __init__(self, add_char: str):
        super().__init__()
        self.addItem(add_char)
        self._add_idx = 0
        self._add_command: tp.Callable or None = None
        self.activated.connect()

    def _prepare_click(self, idx: int):
        if idx == self._add_idx and self._add_command:
            self._add_command()

    def set_add_command(self, add_command: tp.Callable):
        self._add_command = add_command


class QInpIntField(InputWidget, QManyField):

    def __init__(self, fields: int):
        super().__init__(fields, QSpinBox)

    def add_to_struct(self, dict_: dict, key) -> dict:
        if isinstance(dict_[key], tp.Collection):
            for i, value in enumerate(dict_.get(key)):
                self.insert(i, value)
        dict_[key] = self

        return dict_


class QInpCheckBox(InputWidget, QCheckBox):

    def __init__(self):
        super().__init__()

    def add_to_struct(self, dict_: dict, key) -> dict:
        value = dict_[key]
        if isinstance(value, bool):
            self.setChecked(value)
        dict_[key] = self

        return dict_

    def get(self):
        return self.isChecked()


class QInpPathEdit(InputWidget, QPathEdit):

    def __init__(self):
        super().__init__()

    def add_to_struct(self, dict_: dict, key) -> dict:
        value = dict_[key]
        if value:
            self.insert(value)
        dict_[key] = self
        return dict_

    def get(self):
        return self.text()


class QInpMemoryEditComboBox(InputWidget, QLineEditComboBox):
    measurement_units: tuple = ('Б', 'КБ', 'МБ', 'ГБ')

    def __init__(self):
        super().__init__(self.measurement_units)

    def get(self):
        num, num_unit = self.value()
        for i, unit in self.measurement_units:

            if num_unit == unit:
                if i > 0:
                    return num * (1024 * i)
                return num
