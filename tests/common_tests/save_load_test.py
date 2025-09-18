from PySide6.QtWidgets import QMainWindow

import json

from src.gui.interfaces import View, Presenter, ConfigStruct, config
from src.gui.gui_model import Saver
from src.gui.gui import launch
from tests.common_tests. base import BaseTest, CaseFields
import src.gui.gui_const as const

import typing as tp
from pathlib import Path


class ModelTest(BaseTest, View):

    def __init__(self, cases_dir: Path, *args):

        BaseTest.__init__(self, cases_dir)
        View.__init__(self)

        self._config: ConfigStruct = config
        self.filters_add: tp.Callable = None
        self.config_add: tp.Callable = None
        self.filters_change: tp.Callable = None
        self.config_change: tp.Callable = None

    def insert_config(self, config_: ConfigStruct):
        self._config = config_

    def get_config(self) -> ConfigStruct:
        return self._config

    @tp.overload
    def insert(self, widget: str, input_: str): pass
    def insert(self, widget: str, input_: tuple):
        self._config[widget] = input_

    def add_control_btn(self, key: str, label: str, field: str, command: tp.Callable, alignment: tp.Any = None, tooltip: str | None = None):

        match key:
            case const.Elements.BTN_ADD_CONF:
                self.config_add = command
            case const.Elements.BTN_ADD_FILTERS:
                self.filters_add = command

    def add_control_combobox(self, key: str, field: str, command: tp.Callable, values: tuple | list, alignment: tp.Any = None, tooltip: str | None = None):
        match key:
            case const.Elements.CONFIG_SWITCH:
                self.config_change = command
            case const.Elements.FILTERS_SWITCH:
                self.filters_change = command

    @property
    def root_field(self):
        """Return the name of the root field ("main_field" default)."""
        return self.MAIN
