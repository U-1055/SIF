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

STYLE_ERROR = 'error_theme'
STYLE_DARK = 'dark_theme'
STYLE_LIGHT = 'light_style'

styles = {
    STYLE_ERROR: 'error_theme.qss',
    STYLE_LIGHT: 'light_theme.qss',
    STYLE_DARK: 'dark_theme.qss'
}

if __name__ == '__main__':
    pass
