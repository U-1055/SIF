from interfaces import Presenter, ConfigStruct


class LogicManager(Presenter):

    def __init__(self, validation_params: dict, model: object = None, view: object = None):
        super().__init__(model, view)
        self._validation_params: dict = validation_params

    def prepare_data(self, data: ConfigStruct):
        """Обрабатывает данные от View."""
        error_widgets: tuple = self._validate()
        if error_widgets:
            self._view.show_errors(error_widgets)

    def _validate(self) -> tuple:
        """Выполняет валидацию."""
        pass



