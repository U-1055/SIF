import enum

from interfaces import Presenter, ConfigStruct, config


class LogicManager(Presenter):

    # ключи конфига
    INPUT_PARAMS = 3
    INPUT_DIR = 'input_dir'
    TOTAL_IMAGES = 'total_images'
    THREADS = 'threads'

    FILTERS = 'filters'
    FORMAT = 'format'
    WEIGHT = 'weight'
    EXTENSION = 'extension'
    NUMBER_MULTIPLICITY = 'number_multiplicity'
    CONTENT = 'content'
    PREPARED = 'prepared'

    ACTIONS = 'actions'
    RESIZE = 'resize'
    CROP = 'crop'
    REFORMAT = 'reformat'
    SAVE = 'save'
    DELETE = 'delete'
    OUTPUT_DIR = 'output_dir'

    LabelsStruct = {
        INPUT_DIR: ''
    }

    def __init__(self, validation_params: dict, model: object = None, view: object = None):
        super().__init__(model, view)
        self._validation_params: dict = validation_params
        self._config_name: str = self._model.config_name
        self._config_struct: ConfigStruct = self._model.get_config(self._config_name, self._filters_now)
        self._init_data = self._model.get_config_data()

        if self._config_struct is None:
            self._config_struct = config

    def prepare_data(self, data: ConfigStruct):
        """Обрабатывает данные от View."""
        error_widgets: tuple = self._validate()
        if error_widgets:
            self._view.show_errors(error_widgets)

    def change_filters(self, filters_num: int):
        # ToDo: внимание! предполагается что конфиг уже отвалидирован (валидируется после каждого завершения редактирования поля)
        self._model.save_config(self._config_name, self._filters_now, self._config_struct)
        self._config_struct = self._model.get_config(self._config_name, filters_num)
        self._filters_now = filters_num
        self._view.update_config()

    def change_config(self):
        pass

    @property
    def init_data(self) -> dict:
        return self._init_data

    def _validate(self) -> tuple:
        """Выполняет валидацию."""
        pass

    def _get_filters(self, num: int):
        pass


