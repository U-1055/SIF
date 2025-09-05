import abc

from PySide6.QtWidgets import QWidget, QLineEdit, QSpinBox, QComboBox
from abc import abstractmethod


class InputWidget(QWidget):

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
        self.insert(dict_.get(key))
        dict_.update([(key, self)])
        return dict_

    def get(self):
        return self.text()


class QInpSpinBox(InputWidget, QSpinBox):
    
    def add_to_struct(self, dict_: dict, key) -> dict:
        value = dict_.get(key)
        if value:
            self.setValue(int(value))

        dict_.update([(key, self)])
        return dict_

    def get(self):
        return self.text()


class QInpComboBox(InputWidget, QComboBox):
    
    def __init__(self):
        super().__init__()
    
    def add_to_struct(self, dict_: dict, key) -> dict:
        value = dict_.get(key)
        if value:
            self.setItemText(int(value))

        dict_.update([(key, self)])
        return dict_

    def get(self):
        return self.currentText()


