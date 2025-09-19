from enum import Enum

IN_PROGRESS = 'Выполняется...'
START = 'Начать обработку'

CONFIG_NAME = 'config_name'
CONFIGS_LIST = 'configs_list'
FILTERS = 'filters'

validation_rules = {
                   'input_dir': '', 'total_images': '', 'threads': 1,
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

class Elements:
    """Класс, содержащий названия элементов интерфейса"""
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


fields = (
    Elements.INPUT_DIR,
    Elements.TOTAL_IMAGES,
    Elements.THREADS,
    Elements.FORMAT,
    Elements.WEIGHT,
    Elements.SIZE,
    Elements.NAME,
    Elements.EXTENSION,
    Elements.NUMBER_MULTIPLICITY,
    Elements.CONTENT,
    Elements.PREPARED,
    Elements.RESIZE,
    Elements.CROP,
    Elements.REFORMAT,
    Elements.SAVE,
    Elements.DELETE,
    Elements.OUTPUT_DIR,
)
labels = {
    Elements.COMMON_PARAMS: 'Общие параметры',
    Elements.FILTERS: 'Фильтры',
    Elements.ACTIONS: 'Действия',
    Elements.INPUT_DIR: 'Целевая папка',
    Elements.TOTAL_IMAGES: 'Проверить изображений',
    Elements.THREADS: 'Потоки',
    Elements.FORMAT: 'Формат',
    Elements.SIZE: 'Размер изображения',
    Elements.NAME: 'Имя файла',
    Elements.WEIGHT: 'Размер файла',
    Elements.EXTENSION: 'Расширение',
    Elements.NUMBER_MULTIPLICITY: 'Кратность номера изображения',
    Elements.CONTENT: 'Содержимое изображения',
    Elements.PREPARED: 'Обработать изображений',
    Elements.RESIZE: 'Изменить размер на',
    Elements.CROP: 'Обрезать',
    Elements.REFORMAT: 'Конвертировать',
    Elements.SAVE: 'Сохранить в выходной папке',
    Elements.DELETE: 'Удалить из целевой папки',
    Elements.OUTPUT_DIR: 'Выходная папка',
    Elements.BTN_START: 'Начать обработку',
    Elements.CONFIG_SWITCH: 'Изменить конфиг',
    Elements.FILTERS_SWITCH: 'Изменить настройки',
    Elements.BTN_SAVE: 'Сохранить конфиг',
    Elements.BTN_DARK_THEME: 'Темная тема',
    Elements.BTN_LIGHT_THEME: 'Светлая тема',
    Elements.BTN_ADD_FILTERS: 'Добавить настройки',
    Elements.BTN_ADD_CONF: 'Добавить конфиг'
}
tooltips = {
    Elements.COMMON_PARAMS: 'Общие параметры',
    Elements.FILTERS: 'Фильтры',
    Elements.ACTIONS: 'Действия',
    Elements.INPUT_DIR: 'Целевая папка',
    Elements.TOTAL_IMAGES: 'Проверить изображений',
    Elements.THREADS: 'Потоки',
    Elements.FORMAT: 'Формат',
    Elements.SIZE: 'Размер изображения',
    Elements.NAME: 'Имя файла',
    Elements.WEIGHT: 'Размер файла',
    Elements.EXTENSION: 'Расширение',
    Elements.NUMBER_MULTIPLICITY: 'Кратность номера изображения',
    Elements.CONTENT: 'Содержимое изображения',
    Elements.PREPARED: 'Обработать изображений',
    Elements.RESIZE: 'Изменить размер на',
    Elements.CROP: 'Обрезать',
    Elements.REFORMAT: 'Конвертировать',
    Elements.SAVE: 'Сохранить в выходной папке',
    Elements.DELETE: 'Удалить из целевой папки',
    Elements.OUTPUT_DIR: 'Выходная папка',
    Elements.BTN_START: 'Начать обработку',
    Elements.CONFIG_SWITCH: 'Изменить конфиг',
    Elements.FILTERS_SWITCH: 'Изменить настройки',
    Elements.BTN_SAVE: 'sth'
}

STYLE_ERROR = 'error_theme'
STYLE_DARK = 'dark_theme'
STYLE_LIGHT = 'light_style'

styles = {
    STYLE_LIGHT: 'light_theme.qss',
    STYLE_DARK: 'dark_theme.qss',
    STYLE_ERROR: 'error_theme.qss'
}

EQUAL = '='
MORE = '>'
LESS = '<'

if __name__ == '__main__':
    pass
