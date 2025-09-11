import enum

from interfaces import Presenter, ConfigStruct, config


class LogicManager(Presenter):

    MAIN_FIELD = 'main_field'
    CONFIGS_LIST = 'configs_list'

    # ключи конфига
    INPUT_PARAMS = 3

    COMMON_PARAMS = 'common_params'
    INPUT_DIR = 'input_dir'
    TOTAL_IMAGES = 'total_images'
    THREADS = 'threads'

    FILTERS = 'filters'
    FORMAT = 'format'
    SIZE = 'size'
    WEIGHT = 'weight'
    EXTENSION = 'extension'
    NAME = 'name'
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

    BTN_START = 'btn_start'
    BTN_SAVE = 'btn_save'
    BTN_DELETE = 'btn_delete'
    TEXT_SHOWER = 'text_shower'
    CONFIG_SWITCH = 'config_switch'
    FILTERS_SWITCH = 'filters_switch'

    fields = (
        INPUT_DIR,
        TOTAL_IMAGES,
        THREADS,

        FORMAT,
        WEIGHT,
        SIZE,
        NAME,
        EXTENSION,
        NUMBER_MULTIPLICITY,
        CONTENT,
        PREPARED,

        RESIZE,
        CROP,
        REFORMAT,
        SAVE,
        DELETE,
        OUTPUT_DIR,
    )

    labels = {
        COMMON_PARAMS: 'Общие параметры',
        FILTERS: 'Фильтры',
        ACTIONS: 'Действия',
        INPUT_DIR: 'Целевая папка',
        TOTAL_IMAGES: 'Проверить изображений',
        THREADS: 'Потоки',
        FORMAT: 'Формат',
        SIZE: 'Размер изображения',
        NAME: 'Имя файла',
        WEIGHT: 'Размер файла',
        EXTENSION: 'Расширение',
        NUMBER_MULTIPLICITY: 'Кратность номера изображения',
        CONTENT: 'Содержимое изображения',
        PREPARED: 'Обработать изображений',
        RESIZE: 'Изменить размер на',
        CROP: 'Обрезать',
        REFORMAT: 'Конвертировать',
        SAVE: 'Сохранить в выходной папке',
        DELETE: 'Удалить из целевой папки',
        OUTPUT_DIR: 'Выходная папка',
        BTN_START: 'Начать обработку',
        CONFIG_SWITCH: 'Изменить конфиг',
        FILTERS_SWITCH: 'Изменить настройки',
        BTN_SAVE: 'Сохранить конфиг'
    }

    tooltips = {   # ToDo: написать подсказки
        COMMON_PARAMS: 'Общие параметры',
        FILTERS: 'Фильтры',
        ACTIONS: 'Действия',
        INPUT_DIR: 'Целевая папка',
        TOTAL_IMAGES: 'Проверить изображений',
        THREADS: 'Потоки',
        FORMAT: 'Формат',
        SIZE: 'Размер изображения',
        NAME: 'Имя файла',
        WEIGHT: 'Размер файла',
        EXTENSION: 'Расширение',
        NUMBER_MULTIPLICITY: 'Кратность номера изображения',
        CONTENT: 'Содержимое изображения',
        PREPARED: 'Обработать изображений',
        RESIZE: 'Изменить размер на',
        CROP: 'Обрезать',
        REFORMAT: 'Конвертировать',
        SAVE: 'Сохранить в выходной папке',
        DELETE: 'Удалить из целевой папки',
        OUTPUT_DIR: 'Выходная папка',
        BTN_START: 'Начать обработку',
        CONFIG_SWITCH: 'Изменить конфиг',
        FILTERS_SWITCH: 'Изменить настройки',
        BTN_SAVE: 'sth'
    }

    allowed_params = {
        FORMAT: ('JPEG', 'PNG', 'BMP'),
        EXTENSION: ('jpg', 'png', 'bmp'),
        REFORMAT: ('JPEG', 'PNG', 'BMP'),
    }

    def __init__(self, validation_params: dict, model: object = None, view: object = None):
        super().__init__(model, view)
        self._validation_params: dict = validation_params
        self._config_name: str = self._model.config_name
        self._config_struct: ConfigStruct = self._model.get_config(self._config_name, self._filters_now)
        self._init_data = self._model.get_config_data()

        self._configs: list = self._init_data[self.CONFIGS_LIST]
        self._filters_num: int = self._init_data[self.FILTERS]

        if self._config_struct is None:
            self._config_struct = config
        self._config_view()
        self._update_config(self._config_struct)

    def _config_view(self):

        self._view.add_control_btn(self.BTN_SAVE, self.labels[self.BTN_SAVE], self.MAIN_FIELD, self.save_config)
        self._view.add_control_combobox(self.CONFIG_SWITCH, self.MAIN_FIELD, self.change_config, self._configs)

        self._view.add_field(self.COMMON_PARAMS, self.labels[self.COMMON_PARAMS], self.MAIN_FIELD, None)
        self._view.add_field(self.FILTERS, self.labels[self.FILTERS], self.MAIN_FIELD, None)
        self._view.add_field(self.ACTIONS, self.labels[self.ACTIONS], self.MAIN_FIELD, None)

        self._view.add_control_btn(self.BTN_START, self.labels[self.BTN_START], self.MAIN_FIELD, self.prepare_data, None)

        self._view.add_path_edit(self.INPUT_DIR, self.labels[self.INPUT_DIR], self.COMMON_PARAMS, None)
        self._view.add_counter(self.TOTAL_IMAGES, self.labels[self.TOTAL_IMAGES], self.COMMON_PARAMS, 0, 10 ** 6)
        self._view.add_counter(self.THREADS, self.labels[self.THREADS], self.COMMON_PARAMS, 0, 12)

        self._view.add_control_combobox(self.FILTERS_SWITCH, self.FILTERS, self.change_filters, [str(num) for num in range(self._filters_num)])
        self._view.add_combobox(self.FORMAT, self.labels[self.FORMAT], self.FILTERS, self.allowed_params[self.FORMAT], None)
        self._view.add_wdg_many_fields(self.SIZE, self.labels[self.SIZE], self.FILTERS, 2, 0, 10 ** 4)
        self._view.add_line_edit(self.NAME, self.labels[self.NAME], self.FILTERS)
        self._view.add_memory_counter(self.WEIGHT, self.labels[self.WEIGHT], self.FILTERS, None)
        self._view.add_combobox(self.EXTENSION, self.labels[self.EXTENSION], self.FILTERS, self.allowed_params[self.EXTENSION], None)
        self._view.add_counter(self.NUMBER_MULTIPLICITY, self.labels[self.NUMBER_MULTIPLICITY], self.FILTERS, 0, 10 ** 3)
        self._view.add_counter(self.PREPARED, self.labels[self.PREPARED], self.FILTERS, 0, 10 ** 6)
        self._view.add_line_edit(self.CONTENT, self.labels[self.CONTENT], self.FILTERS, None)

        self._view.add_wdg_many_fields(self.RESIZE, self.labels[self.RESIZE], self.ACTIONS, 2, 0, 10 ** 4)
        self._view.add_wdg_many_fields(self.CROP, self.labels[self.CROP], self.ACTIONS, 4, 0, 10 ** 4)
        self._view.add_combobox(self.REFORMAT, self.labels[self.REFORMAT], self.ACTIONS, self.allowed_params[self.REFORMAT], None)
        self._view.add_switch(self.SAVE, self.labels[self.SAVE], self.ACTIONS, True, None)
        self._view.add_switch(self.DELETE, self.labels[self.DELETE], self.ACTIONS, False, None)
        self._view.add_path_edit(self.OUTPUT_DIR, self.labels[self.OUTPUT_DIR], self.ACTIONS, None)

    def _get_view_data(self, config_: ConfigStruct) -> ConfigStruct:
        """Get data from View."""
        for wdg_key in config_:

            if wdg_key == self.FILTERS:
                config_[wdg_key][0] = self._get_view_data(config_[wdg_key][0])
            elif wdg_key == self.ACTIONS:
                config_[wdg_key] = self._get_view_data(config_[wdg_key])
            elif wdg_key in self.fields:
                data = self._view.get(wdg_key)
                if data is not None:
                    config_[wdg_key] = data

        return config_

    def prepare_data(self):
        """Обрабатывает данные от View."""
        self._config_struct = self._get_view_data(self._config_struct)

        error_widgets: tuple = self._validate()
        if error_widgets:
            self._view.show_errors(error_widgets)

        print('The data was prepared')

    def change_filters(self, filters_num: int):
        # ToDo: внимание! предполагается что конфиг уже отвалидирован (валидируется после каждого завершения редактирования поля)
        print(f'Filters: {self._filters_num}, Filter: {filters_num}')
        self._model.save_config(self._config_name, self._filters_now, self._config_struct)
        self._config_struct = self._model.get_config(self._config_name, filters_num)
        self._filters_now = filters_num

        self._update_config(self._config_struct)

    def change_config(self, num: int):
        print(f'New config: {num}')
        self._config_name = self._configs[num]
        config_ = self._model.get_config(self._config_name, self._filters_now)
        if config_:
            self._config_struct = config_
        self._update_config(self._config_struct)

    def save_config(self):
        self._config_struct = self._get_view_data(self._config_struct)
        self._model.save_config(self._config_name, self._filters_now, self._config_struct)

    def _update_config(self, config_: dict):
        for wdg_key in config_:

            if wdg_key == self.FILTERS:
                self._update_config(config_[wdg_key][0])

            elif wdg_key == self.ACTIONS:
                self._update_config(config_[wdg_key])

            elif wdg_key in self.fields:
                self._view.clear(wdg_key)
                if config_[wdg_key] != '':
                    self._view.insert(wdg_key, config_[wdg_key])
        self._view.insert_control_combobox(self.CONFIG_SWITCH, self._config_name)
        self._view.insert_control_combobox(self.FILTERS_SWITCH, str(self._filters_now))

    @property
    def init_data(self) -> dict:
        return self._init_data

    def _validate(self) -> tuple:
        """Выполняет валидацию."""
        pass

    def _get_filters(self, num: int):
        pass
