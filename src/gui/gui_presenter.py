import enum

from interfaces import Presenter, ConfigStruct, config, Model, View
import gui_const as const
from src.nnfcv.program_logic import Preparer


class LogicManager(Presenter):

    allowed_params = {
        const.Elements.FORMAT: ('Не учитывать', 'JPEG', 'PNG', 'BMP'),
        const.Elements.EXTENSION: ('Не учитывать', 'jpg', 'png', 'bmp'),
        const.Elements.REFORMAT: ('Не учитывать', 'JPEG', 'PNG', 'BMP'),
    }
    ADD_CONF_TITLE = 'Новый конфиг'
    fields = const.fields

    def __init__(self,
                 validation_params: dict,
                 styles_table: tuple,
                 elements: const.Elements,
                 labels: dict,
                 tooltips: dict,
                 model: Model = None, view: View = None):
        super().__init__(validation_params, model, view)
        if model:
            self._model = model
        if view:
            self._view = view
            self.MAIN_FIELD = self._view.root_field

        self.STYLE_LIGHT, self.STYLE_DARK, self.STYLE_ERR = styles_table

        self._validation_params: dict = validation_params
        self._config_name: str = self._model.config_name
        self._config_struct: ConfigStruct = self._model.get_config(self._config_name, self._filters_now)

        self._els = elements
        self.labels = labels
        self.tooltips = tooltips

        self._current_style: str = self._model.current_style

        self._update_configs_data()
        self._config_view()
        self._update_config(self._config_struct)

    def _update_configs_data(self):
        """Обновляет данные о конфиге"""
        self._init_data = self._model.get_config_data()
        self._configs: list = self._init_data[self._els.CONFIGS_LIST]
        self._filters_num: int = self._init_data[self._els.FILTERS]

        if self._config_struct is None:
            self._config_struct = config

    def _config_view(self):
        """Устанавливает компоновку интерфейса"""

        align_right = self._view.alignment_right
        align_left = self._view.alignment_left
        align_top = self._view.alignment_top
        align_bottom = self._view.alignment_bottom
        light_style = self._model.get_style(self.STYLE_LIGHT)
        dark_style = self._model.get_style(self.STYLE_DARK)

        self._view.apply_main_style(self._model.get_style(self._current_style))

        self._view.add_field(self._els.TOOLS_FIELD, None, self._els.MAIN_FIELD, 'h')
        self._view.add_field(self._els.COMMON_PARAMS, self.labels.get(self._els.COMMON_PARAMS), self._els.MAIN_FIELD, 'f', None)
        self._view.add_field(self._els.FILTERS_CONTROL_FIELD, None, self._els.MAIN_FIELD, 'h')
        self._view.add_field(self._els.SETTINGS_FIELD, None, self._els.MAIN_FIELD, 'h')
        self._view.add_field(self._els.THEME_CHANGE_FIELD, '', self._els.TOOLS_FIELD, 'v')

        self._view.add_control_btn(self._els.BTN_LIGHT_THEME, self.labels.get(self._els.BTN_LIGHT_THEME), self._els.THEME_CHANGE_FIELD,
                                   lambda: self._change_theme(self.STYLE_LIGHT, light_style), align_left)
        self._view.add_control_btn(self._els.BTN_DARK_THEME, self.labels.get(self._els.BTN_DARK_THEME), self._els.THEME_CHANGE_FIELD,
                                   lambda: self._change_theme(self.STYLE_DARK, dark_style), align_left)
        self._view.apply_style(self._els.BTN_LIGHT_THEME, light_style)
        self._view.apply_style(self._els.BTN_DARK_THEME, dark_style)

        self._view.add_control_btn(self._els.BTN_START, self.labels.get(self._els.BTN_START), self._els.TOOLS_FIELD, self.prepare_data,
                                   align_left)
        self._view.add_control_btn(self._els.BTN_SAVE, self.labels.get(self._els.BTN_SAVE), self._els.TOOLS_FIELD, self.save_config, align_left)
        self._view.add_control_btn(self._els.BTN_ADD_CONF, self.labels.get(self._els.BTN_ADD_CONF), self._els.TOOLS_FIELD, self.add_config, align_left)
        self._view.add_control_combobox(self._els.CONFIG_SWITCH, self._els.TOOLS_FIELD, self.change_config, self._configs, align_left,
                                        self.tooltips[self._els.CONFIG_SWITCH])

        self._view.add_label('settings_lbl', 'Текущие настройки:', self._els.FILTERS_CONTROL_FIELD, align_left)
        self._view.add_control_combobox(self._els.FILTERS_SWITCH, self._els.FILTERS_CONTROL_FIELD, self.change_filters,
                                        [str(num) for num in range(self._filters_num)], align_left, self.tooltips.get(self._els.FILTERS_SWITCH))
        self._view.add_control_btn(self._els.BTN_ADD_FILTERS, self.labels.get(self._els.BTN_ADD_FILTERS), self._els.FILTERS_CONTROL_FIELD,
                                   self.add_filters, align_left)

        self._view.add_field(self._els.FILTERS, self.labels.get(self._els.FILTERS), self._els.SETTINGS_FIELD, 'f', None)
        self._view.add_field(self._els.ACTIONS, self.labels.get(self._els.ACTIONS), self._els.SETTINGS_FIELD, 'f', None)
        self._view.add_field(self._els.CONTROL_FIELD, None, self._els.MAIN_FIELD, 'h')

        self._view.add_text_shower(self._els.TEXT_SHOWER, '', self._els.CONTROL_FIELD, align_left)

        self._view.add_path_edit(self._els.INPUT_DIR, self.labels.get(self._els.INPUT_DIR), self._els.COMMON_PARAMS, align_left, self.tooltips.get(self._els.INPUT_DIR))
        self._view.add_counter(self._els.TOTAL_IMAGES, self.labels.get(self._els.TOTAL_IMAGES), self._els.COMMON_PARAMS, 0, 10 ** 6, align_left, self.tooltips.get(self._els.TOTAL_IMAGES))
        self._view.add_counter(self._els.THREADS, self.labels.get(self._els.THREADS), self._els.COMMON_PARAMS, 1, 12, align_left, self.tooltips.get(self._els.THREADS))

        self._view.add_combobox(self._els.FORMAT, self.labels.get(self._els.FORMAT), self._els.FILTERS, self.allowed_params[self._els.FORMAT], align_left, self.tooltips.get(self._els.FORMAT))
        self._view.add_line_edit(self._els.NAME, self.labels.get(self._els.NAME), self._els.FILTERS, align_left, self.tooltips.get(self._els.NAME))
        self._view.add_line_edit(self._els.EXTENSION, self.labels.get(self._els.EXTENSION), self._els.FILTERS, align_left, self.tooltips.get(self._els.EXTENSION))
        self._view.add_counter(self._els.NUMBER_MULTIPLICITY, self.labels.get(self._els.NUMBER_MULTIPLICITY), self._els.FILTERS, 1, 10 ** 3, align_left, self.tooltips.get(self._els.NUMBER_MULTIPLICITY))
        self._view.add_counter(self._els.PREPARED, self.labels.get(self._els.PREPARED), self._els.FILTERS, 0, 10 ** 6, align_left, self.tooltips.get(self._els.PREPARED))
        self._view.add_line_edit(self._els.CONTENT, self.labels.get(self._els.CONTENT), self._els.FILTERS, align_left, self.tooltips.get(self._els.CONTENT))
        self._view.add_memory_counter(self._els.WEIGHT, self.labels.get(self._els.WEIGHT), self._els.FILTERS, align_left, self.tooltips.get(self._els.WEIGHT))
        self._view.add_wdg_resolution_edit(self._els.SIZE, self.labels.get(self._els.SIZE), self._els.FILTERS, 0, 2 ** 13, align_left, self.tooltips.get(self._els.SIZE))

        self._view.add_wdg_many_fields(self._els.RESIZE, self.labels.get(self._els.RESIZE), self._els.ACTIONS, 2, 0, 10 ** 4, align_left, self.tooltips.get(self._els.RESIZE))
        self._view.add_wdg_many_fields(self._els.CROP, self.labels.get(self._els.CROP), self._els.ACTIONS, 4, 0, 10 ** 4, align_left, self.tooltips.get(self._els.CROP))
        self._view.add_combobox(self._els.REFORMAT, self.labels.get(self._els.REFORMAT), self._els.ACTIONS, self.allowed_params[self._els.REFORMAT], align_left, self.tooltips.get(self._els.REFORMAT))
        self._view.add_path_edit(self._els.OUTPUT_DIR, self.labels.get(self._els.OUTPUT_DIR), self._els.ACTIONS, align_left, self.tooltips.get(self._els.OUTPUT_DIR))
        self._view.add_switch(self._els.SAVE, self.labels.get(self._els.SAVE), self._els.ACTIONS, True, align_left, self.tooltips.get(self._els.SAVE))
        self._view.add_switch(self._els.DELETE, self.labels.get(self._els.DELETE), self._els.ACTIONS, False, align_left, self.tooltips.get(self._els.DELETE))

    def _change_theme(self, style_name: str, style: str):
        self._model.change_style(style_name)
        self._view.apply_main_style(style)

    def _get_view_data(self, config_: ConfigStruct) -> ConfigStruct:
        """Get data from View."""
        for wdg_key in config_:

            if wdg_key == self._els.FILTERS:
                config_[wdg_key][0] = self._get_view_data(config_[wdg_key][0])
            elif wdg_key == self._els.ACTIONS:
                config_[wdg_key] = self._get_view_data(config_[wdg_key])
            elif wdg_key in self.fields:
                data = self._view.get(wdg_key)
                if data is not None:
                    config_[wdg_key] = data

        return config_

    def _prepare_params(self, config_: ConfigStruct):
        """Приводит параметры к состоянию, требуемому обработчиком."""
        config_[self._els.TOTAL_IMAGES] = (0, int(config_[self._els.TOTAL_IMAGES]))
        config_[self._els.THREADS] = int(config_[self._els.THREADS])

        filters = config_[self._els.FILTERS]

        for param in config_[self._els.FILTERS]:
            match param:
                case self._els.SIZE:
                    for dim in filters[self._els.SIZE]:
                        dim[0] = int(dim[0])
                    filters[self._els.SIZE] = (filters[self._els.SIZE], )

                case self._els.WEIGHT:
                    filters[self._els.WEIGHT][0] = int(filters[self._els.WEIGHT][0])

                case self._els.NUMBER_MULTIPLICITY:
                    filters[self._els.NUMBER_MULTIPLICITY] = (int(filters[self._els.NUMBER_MULTIPLICITY][0]), )

    def prepare_data(self):
        """Обрабатывает данные от View."""
        view_data = self._get_view_data(self._config_struct)

        self._config_struct = self._get_view_data(self._config_struct)

        error_widgets: tuple = self._validate()
        if error_widgets:
            self._view.show_errors(error_widgets)
            return

        self._model.save_config(self._config_name, self._filters_now, config)
        Preparer([self._config_struct])
        print('The data was prepared')

    def change_filters(self, filters_num: int):
        # предполагается что конфиг уже отвалидирован
        # (валидируется после каждого завершения редактирования поля)
        print(f'Filters: {self._filters_num}, Filter: {filters_num}')

        self._model.save_config(self._config_name, self._filters_now, self._config_struct)
        self._config_struct = self._model.get_config(self._config_name, filters_num)
        self._filters_now = filters_num

        self._update_config(self._config_struct)
        self._view.insert_control_combobox(self._els.FILTERS_SWITCH, str(filters_num))

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
                self._view.insert_control_combobox(self._els.CONFIG_SWITCH, name)
                self.change_config(self._configs.index(name))
                self._config_name = name

    def add_filters(self):
        self._model.add_filters(self._config_name)
        self._update_configs_data()
        self._view.insert_control_combobox(self._els.FILTERS_SWITCH, str(self._filters_num - 1))

    def _update_config(self, config_: dict):
        for wdg_key in config_:

            if wdg_key == self._els.FILTERS:
                self._update_config(config_[wdg_key][0])

            elif wdg_key == self._els.ACTIONS:
                self._update_config(config_[wdg_key])

            elif wdg_key in self.fields:
                self._view.clear(wdg_key)
                if config_[wdg_key] != '':
                    self._view.insert(wdg_key, config_[wdg_key])
        self._view.insert_control_combobox(self._els.CONFIG_SWITCH, self._config_name)
        self._view.insert_control_combobox(self._els.FILTERS_SWITCH, str(self._filters_now))

    @property
    def init_data(self) -> dict:
        return self._init_data

    def _validate(self) -> tuple:
        """Выполняет валидацию."""
        pass

    def _get_filters(self, num: int):
        pass

