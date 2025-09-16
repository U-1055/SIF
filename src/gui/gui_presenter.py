import enum

from interfaces import Presenter, ConfigStruct, config
import gui_const as const


class LogicManager(Presenter):

    MAIN_FIELD = 'main_field'
    CONFIGS_LIST = 'configs_list'
    TOOLS_FIELD = 'tools_field'
    SETTINGS_FIELD = 'settings_field'
    CONTROL_FIELD = 'control_field'
    THEME_CHANGE_FIELD = 'theme_change_field'

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
    BTN_ADD_CONF = 'btn_add_conf'
    BTN_ADD_FILTERS = 'btn_add_filters'
    BTN_DELETE = 'btn_delete'
    BTN_LIGHT_THEME = 'btn_light_theme'
    BTN_DARK_THEME = 'btn_dark_theme'
    TEXT_SHOWER = 'text_shower'
    CONFIG_SWITCH = 'config_switch'
    FILTERS_SWITCH = 'filters_switch'
    FILTERS_CONTROL_FIELD = 'filters_control_field'

    ADD_CONF_TITLE = 'Введите название конфига'
    LBL_NONE = 'Не учитывать'

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
        THREADS: 'Процессы',
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
        BTN_ADD_CONF: 'Добавить конфиг',
        BTN_ADD_FILTERS: 'Добавить настройки',
        CONFIG_SWITCH: 'Изменить конфиг',
        FILTERS_SWITCH: 'Изменить настройки',
        BTN_SAVE: 'Сохранить конфиг',
        ADD_CONF_TITLE: 'Введите название нового конфига',
        BTN_LIGHT_THEME: 'Светлая тема',
        BTN_DARK_THEME: 'Тёмная тема'
    }

    tooltips = {
        COMMON_PARAMS: 'Общие параметры',
        FILTERS: 'Фильтры',
        ACTIONS: 'Действия',
        INPUT_DIR: 'Папка, изображения в которой будут обработаны программой',
        TOTAL_IMAGES: 'Максимальное число изображений, которые проверит программа',
        THREADS: 'Число процессов, используемых при обработке',
        FORMAT: 'Будут обработаны только изображения этого формата',
        SIZE: 'Будут обработаны изображения, соответствующие указанному разрешению (>, < или =)',
        NAME: 'Название файла изображения. Используйте * для маски, означающей любую последовательность символов (или их отсутствие).'
              '\nНажмите на чекбокс для использования синтаксиса регулярных выражений',
        WEIGHT: 'Будут обработаны только изображения, соответствующие указанному размеру\n (в заданных единицах измерения)',
        EXTENSION: 'Будут обработаны только файлы с заданным расширением',
        NUMBER_MULTIPLICITY: 'Изображение будет обработано, если его порядковый номер в папке нацело делится на указанное число. '
                             '\nПорядковый номер изображения определяется путём лексикографической сортировки названий',
        CONTENT: 'Изображение будет обработано, если ответ нейронной сети для него соответствует указанному в поле',
        PREPARED: 'Максимальное число изображений, соответствующих фильтрам',
        RESIZE: 'Размер соответствующих изображений будет изменён на указанный \n(Пропорции не сохраняются!)',
        CROP: 'Соответствующие изображения будут обрезаны до указанного размера',
        REFORMAT: 'Конвертировать изображение в заданный формат',
        SAVE: 'Сохранить соответствующее изображение в выходную папку',
        DELETE: 'Удалить соответствующее изображение в целевой папке',
        OUTPUT_DIR: f'Папка, в которую будут сохранены соответствующие изображения\n (при выбранном параметре {labels[SAVE]})',
        BTN_START: 'Начать обработку',
        BTN_ADD_CONF: 'Добавить новую конфигурацию обработки',
        BTN_ADD_FILTERS: 'Добавить настройки обработки изображений. \nВ одной конфигурации может быть несколько таких настроек.',
        CONFIG_SWITCH: 'Изменить конфиг',
        FILTERS_SWITCH: 'Изменить настройки обработки. \nВ одной конфигурации может быть несколько таких настроек',
        BTN_SAVE: 'Сохранить конфиг'
    }

    allowed_params = {
        FORMAT: (LBL_NONE, 'JPEG', 'PNG', 'BMP'),
        EXTENSION: (LBL_NONE, 'jpg', 'png', 'bmp'),
        REFORMAT: (LBL_NONE, 'JPEG', 'PNG', 'BMP'),
    }

    def __init__(self, validation_params: dict, styles_table: tuple, model=None, view=None):
        super().__init__(model, view)
        if model:
            self._model = model
        if view:
            self._view = view
            self.MAIN_FIELD = self._view.root_field

        self.STYLE_LIGHT, self.STYLE_DARK, self.STYLE_ERR = styles_table

        self._validation_params: dict = validation_params
        self._config_name: str = self._model.config_name
        self._config_struct: ConfigStruct = self._model.get_config(self._config_name, self._filters_now)

        self._current_style: str = self._model.current_style

        self._update_configs_data()
        self._config_view()
        self._update_config(self._config_struct)

    def _update_configs_data(self):
        self._init_data = self._model.get_config_data()
        self._configs: list = self._init_data[self.CONFIGS_LIST]
        self._filters_num: int = self._init_data[self.FILTERS]

        if self._config_struct is None:
            self._config_struct = config

    def _config_view(self):

        align_right = self._view.alignment_right
        align_left = self._view.alignment_left
        align_top = self._view.alignment_top
        align_bottom = self._view.alignment_bottom
        light_style = self._model.get_style(self.STYLE_LIGHT)
        dark_style = self._model.get_style(self.STYLE_DARK)

        self._view.apply_main_style(self._model.get_style(self._current_style))

        self._view.add_field(self.TOOLS_FIELD, None, self.MAIN_FIELD, 'h')
        self._view.add_field(self.COMMON_PARAMS, self.labels[self.COMMON_PARAMS], self.MAIN_FIELD, 'f', None)
        self._view.add_field(self.FILTERS_CONTROL_FIELD, None, self.MAIN_FIELD, 'h')
        self._view.add_field(self.SETTINGS_FIELD, None, self.MAIN_FIELD, 'h')
        self._view.add_field(self.THEME_CHANGE_FIELD, '', self.TOOLS_FIELD, 'v')

        self._view.add_control_btn(self.BTN_LIGHT_THEME, self.labels[self.BTN_LIGHT_THEME], self.THEME_CHANGE_FIELD,
                                   lambda: self._change_theme(self.STYLE_LIGHT, light_style))
        self._view.add_control_btn(self.BTN_DARK_THEME, self.labels[self.BTN_DARK_THEME], self.THEME_CHANGE_FIELD,
                                   lambda: self._change_theme(self.STYLE_DARK, dark_style))
        self._view.apply_style(self.BTN_LIGHT_THEME, light_style)
        self._view.apply_style(self.BTN_DARK_THEME, dark_style)

        self._view.add_control_btn(self.BTN_START, self.labels[self.BTN_START], self.TOOLS_FIELD, self.prepare_data,
                                   align_left)
        self._view.add_control_btn(self.BTN_SAVE, self.labels[self.BTN_SAVE], self.TOOLS_FIELD, self.save_config, align_left)
        self._view.add_control_btn(self.BTN_ADD_CONF, self.labels[self.BTN_ADD_CONF], self.TOOLS_FIELD, self.add_config, align_left)
        self._view.add_control_combobox(self.CONFIG_SWITCH, self.TOOLS_FIELD, self.change_config, self._configs, align_left,
                                        self.tooltips[self.CONFIG_SWITCH])

        self._view.add_label('settings_lbl', 'Текущие настройки:', self.FILTERS_CONTROL_FIELD, align_left)
        self._view.add_control_combobox(self.FILTERS_SWITCH, self.FILTERS_CONTROL_FIELD, self.change_filters,
                                        [str(num) for num in range(self._filters_num)], align_left, self.tooltips[self.FILTERS_SWITCH])
        self._view.add_control_btn(self.BTN_ADD_FILTERS, self.labels[self.BTN_ADD_FILTERS], self.FILTERS_CONTROL_FIELD,
                                   self.add_filters, align_left)

        self._view.add_field(self.FILTERS, self.labels[self.FILTERS], self.SETTINGS_FIELD, 'f', None)
        self._view.add_field(self.ACTIONS, self.labels[self.ACTIONS], self.SETTINGS_FIELD, 'f', None)
        self._view.add_field(self.CONTROL_FIELD, None, self.MAIN_FIELD, 'h')

        self._view.add_text_shower(self.TEXT_SHOWER, '', self.CONTROL_FIELD, align_left)

        self._view.add_path_edit(self.INPUT_DIR, self.labels[self.INPUT_DIR], self.COMMON_PARAMS, align_left, self.tooltips[self.INPUT_DIR])
        self._view.add_counter(self.TOTAL_IMAGES, self.labels[self.TOTAL_IMAGES], self.COMMON_PARAMS, 0, 10 ** 6, align_left, self.tooltips[self.TOTAL_IMAGES])
        self._view.add_counter(self.THREADS, self.labels[self.THREADS], self.COMMON_PARAMS, 1, 12, align_left, self.tooltips[self.THREADS])

        self._view.add_combobox(self.FORMAT, self.labels[self.FORMAT], self.FILTERS, self.allowed_params[self.FORMAT], align_left, self.tooltips[self.FORMAT])
        self._view.add_line_edit(self.NAME, self.labels[self.NAME], self.FILTERS, align_left, self.tooltips[self.NAME])
        self._view.add_line_edit(self.EXTENSION, self.labels[self.EXTENSION], self.FILTERS, align_left, self.tooltips[self.EXTENSION])
        self._view.add_counter(self.NUMBER_MULTIPLICITY, self.labels[self.NUMBER_MULTIPLICITY], self.FILTERS, 1, 10 ** 3, align_left, self.tooltips[self.NUMBER_MULTIPLICITY])
        self._view.add_counter(self.PREPARED, self.labels[self.PREPARED], self.FILTERS, 0, 10 ** 6, align_left, self.tooltips[self.PREPARED])
        self._view.add_line_edit(self.CONTENT, self.labels[self.CONTENT], self.FILTERS, align_left, self.tooltips[self.CONTENT])
        self._view.add_memory_counter(self.WEIGHT, self.labels[self.WEIGHT], self.FILTERS, align_left, self.tooltips[self.WEIGHT])
        self._view.add_wdg_many_fields(self.SIZE, self.labels[self.SIZE], self.FILTERS, 2, 0, 10 ** 4, align_left, self.tooltips[self.SIZE])

        self._view.add_wdg_many_fields(self.RESIZE, self.labels[self.RESIZE], self.ACTIONS, 2, 0, 10 ** 4, align_left, self.tooltips[self.RESIZE])
        self._view.add_wdg_many_fields(self.CROP, self.labels[self.CROP], self.ACTIONS, 4, 0, 10 ** 4, align_left, self.tooltips[self.CROP])
        self._view.add_combobox(self.REFORMAT, self.labels[self.REFORMAT], self.ACTIONS, self.allowed_params[self.REFORMAT], align_left, self.tooltips[self.REFORMAT])
        self._view.add_path_edit(self.OUTPUT_DIR, self.labels[self.OUTPUT_DIR], self.ACTIONS, align_left, self.tooltips[self.OUTPUT_DIR])
        self._view.add_switch(self.SAVE, self.labels[self.SAVE], self.ACTIONS, True, align_left, self.tooltips[self.SAVE])
        self._view.add_switch(self.DELETE, self.labels[self.DELETE], self.ACTIONS, False, align_left, self.tooltips[self.DELETE])

    def _change_theme(self, style_name: str, style: dict):
        self._model.change_style(style_name)
        self._view.apply_main_style(style)

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
        self._view.insert_control_combobox(self.FILTERS_SWITCH, str(filters_num))

    def change_config(self, num: int):

        self._config_name = self._configs[num]
        config_ = self._model.get_config(self._config_name, self._filters_now)
        if config_:
            self._config_struct = config_
        self._update_config(self._config_struct)

    def save_config(self):
        self._config_struct = self._get_view_data(self._config_struct)
        self._model.save_config(self._config_name, self._filters_now, self._config_struct)

    def add_config(self):
        name = self._view.show_input_dialog_window(self.ADD_CONF_TITLE)
        if name:
            if name in self._configs:
                self._view.show_errors(self.MAIN_FIELD)
            else:
                self._model.add_config(name)
                self._update_configs_data()
                self._view.insert_control_combobox(self.CONFIG_SWITCH, name)
                self.change_config(self._configs.index(name))
                self._config_name = name

    def add_filters(self):
        self._model.add_filters(self._config_name)
        self._update_configs_data()
        self._view.insert_control_combobox(self.FILTERS_SWITCH, str(self._filters_num - 1))

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
