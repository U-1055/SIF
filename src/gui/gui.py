from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QApplication
from PySide6.QtGui import QIcon

import pathlib

from gui_view import MainWindow
from gui_model import Saver
from gui_presenter import LogicManager
from interfaces import Presenter, View, config
from tests.VP_tests.model import TestModel


def init_view(view: QMainWindow):

    view.setWindowTitle('FCV')

    screen = view.screen()

    width = screen.geometry().width()
    height = screen.geometry().height()

    min_width = int(width * 0.3)
    min_height = int(height * 0.5)

    base_width = int(width * 0.5)
    base_height = int(height * 0.55)

    x = (width - base_width) // 2
    y = (height - base_height) // 2

    max_width = int(width * 0.7)
    max_height = int(height * 0.6)

    view.setGeometry(x, y, base_width, base_height)
    view.setMaximumSize(max_width, max_height)
    view.setMinimumSize(min_width, min_height)
    view.resize(base_width, base_height)

    view.show()


if __name__ == '__main__':
    app = QApplication()
    root = MainWindow()
    init_view(root)
    path = pathlib.Path('..', '..', 'data', 'test_data', 'configs')

    icon = QIcon(r"C:\Users\filat\PycharmProjects\NNFCV\data\gui_data\icons\logo.ico")
    app.setWindowIcon(icon)
    root.setWindowIcon(icon)

    model = TestModel(path, config)
    presenter = LogicManager({}, model, root)
    root.set_presenter(presenter)

    app.exec()
