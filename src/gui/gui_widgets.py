import abc

from PySide6.QtWidgets import QWidget, QLineEdit, QSpinBox, QComboBox, QCheckBox
from abc import abstractmethod
import typing as tp

from src.common_widgets.common_widgets import QManyField, QPathEdit, QLineEditComboBox, QManyIntField


class InputWidget:

    @abstractmethod
    def clear_widget(self):
        pass

    @abstractmethod
    def insert_data(self, input_):
        """Вводит данные в виджет."""

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

    def insert_data(self, text: str):
        self.insert(text)

    def clear_widget(self):
        self.clear()


class QInpSpinBox(InputWidget, QSpinBox):

    def __init__(self, min_: int, max_: int):
        super().__init__(minimum=min_, maximum=max_)
    
    def add_to_struct(self, dict_: dict, key) -> dict:
        value = dict_[key]
        if value:
            self.setValue(int(value))

        dict_[key] = self
        return dict_

    def get(self):
        return self.text()

    def insert_data(self, value: int):
        self.setValue(int(value))

    def clear_widget(self):
        self.clear()


class QInpComboBox(InputWidget, QComboBox):
    
    def __init__(self, values: tp.Sequence[str]):
        super().__init__()
        self._values = values
        self.addItems(values)

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

    def insert_data(self, item_text: str):
        self.setCurrentText(item_text)

    def clear_widget(self):
        if len(self._values) > 0:
            self.setCurrentIndex(0)


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


class QInpIntFields(InputWidget, QManyIntField):

    def __init__(self, fields: int, min_: int, max_: int):
        super().__init__(fields, 'x', min_, max_)

    def add_to_struct(self, dict_: dict, key) -> dict:
        if isinstance(dict_[key], tp.Collection):
            for i, value in enumerate(dict_.get(key)):
                self.insert(i, value)
        dict_[key] = self

        return dict_

    def insert_data(self, values: tuple | list):
        for idx, value in enumerate(values):
            self.insert(idx, value)

    def clear_widget(self):
        for idx, _ in enumerate(self.widgets):
            self.clear(idx)

    def get(self):
        values = []
        for idx, _ in enumerate(self.widgets):
            values.append(self.value(idx))
        return values


class QInpCheckBox(InputWidget, QCheckBox):

    def __init__(self, state: bool):
        super().__init__()
        self._state = state
        self.setChecked(state)

    def add_to_struct(self, dict_: dict, key) -> dict:
        value = dict_[key]
        if isinstance(value, bool):
            self.setChecked(value)
        dict_[key] = self

        return dict_

    def get(self):
        return self.isChecked()

    def insert_data(self, state: bool):
        self.setChecked(state)

    def clear(self):
        self.setChecked(self._state)


class QInpPathEdit(InputWidget, QPathEdit):

    def __init__(self):
        super().__init__(is_dir=True)

    def add_to_struct(self, dict_: dict, key) -> dict:
        value = dict_[key]
        if value:
            self.insert(value)
        dict_[key] = self
        return dict_

    def get(self):
        return self.text()

    def insert_data(self, path: str):
        self.insert(path)

    def clear_widget(self):
        self.clear()


class QInpMemoryEditComboBox(InputWidget, QLineEditComboBox):
    measurement_units: tuple = ('Б', 'КБ', 'МБ', 'ГБ')

    def __init__(self):
        super().__init__(QSpinBox, self.measurement_units)

    def get(self):
        num, num_unit = self.value()
        for i, unit in enumerate(self.measurement_units):

            if num_unit == unit:
                if i > 0:
                    return num * (1024 * i)
                return num

    def insert_data(self, input_: int):
        self.insert(str(input_), self.measurement_units[0])

    def clear_widget(self):
        self.clear()
