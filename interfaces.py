from PySide6.QtWidgets import QWidget
from abc import abstractmethod
from gui_widgets import InputWidget
import typing as tp


ConfigStruct = dict[str, str |  # main dict
                    list[  # filters
                      dict[str, str |  # filter
                           dict[str, str | bool]  # actions
                         ]
                        ]
                   ]

ViewConfigStruct = dict[str, InputWidget |  # main dict
                        list[  # filters
                         dict[str, InputWidget |  # filter
                              dict[str, InputWidget]  # actions
                             ]
                           ]
                       ]

config = {
                   'input_dir': r'C:\Users\filat\OneDrive\Документы\Проект\target_dir', 'total_images': '', 'threads': 1,
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
                                 'delete': True,
                                 'output_dir': ''
                                }
                          }
                         ]
}


class View:

    def __init__(self, presenter: 'Presenter' = None):
        if presenter:
            self._presenter: Presenter | None = presenter
        else:
            self._presenter: Presenter | None = None

    def show_errors(self, widgets: tp.Collection[str]):
        pass

    def set_presenter(self, presenter: 'Presenter' = None):
        self._presenter = presenter

    def show_msg(self, msg: str):
        """Передаёт сообщение в виджет отслеживания обработки."""


class Model:
    pass


class Presenter:
    def __init__(self, model: Model = None, view: View = None):
        self._model: Model = model
        self._view: View = view
        self.config_struct: ConfigStruct = config

    @abstractmethod
    def prepare_data(self, data: ConfigStruct):
        """Обрабатывает данные от View."""
        pass

    def set_model(self, model: Model):
        self._model = model

    def set_view(self, view: View):
        self._view = view

