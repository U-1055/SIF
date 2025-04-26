"""Тесты логики"""
import os


def check_chunks(path: str, chunks: int):
    """Проверка соответствия количества изображений в чанках количеству изображений во входной папке"""
    in_dir = len(os.listdir(path))
    assert in_dir == chunks, (f'Разное количество изображений в папке и в чанках, в папке: {in_dir}; в чанках: {chunks};]\n')

def check_replace(path: str, last_num: int):
    """Проверяет, не было ли изображение в папке заменено выгружаемым путём сравнения предыдущего числа файлов в папке и текущего
       (разница должна быть равна 1)."""
    assert len(os.listdir(path)) > last_num, 'Ошибка: выгруженное изображение заменило изображение в папке!'

def check_dirs(path1: str, path2: str):
    """Проверяет идентичность директорий. Возвращает список имён файлов, существующих ТОЛЬКО в одной из директорий."""
    files1 = os.listdir(path1)
    files2 = os.listdir(path2)

    if files1 == files2:
        return []
    else:
        result = []
        if len(files1) > len(files2):
            num = 0
            for i, element in enumerate(files1): #Предполагается, что порядок расположения элементов в обеих папках одинаков, что и должно быть так
                if element != files2[i]:
                    result.append(files2[i])
                    num += 2
                else: num += 1

        if len(files1) < len(files2):
            num = 0
            for element in (files2):
                if element != files1[num]:
                    result.append(files1[num])
                    num += 2
                else: num += 1
        print(f'Проверка директорий: \n{path1.split('\\')[-1]}: {len(files1)}\n{path2.split('\\')[-1]}: {len(files2)}\n')
        return result

def test_check_dirs(path1: str, path2: str):
    assert os.listdir(path1) == os.listdir(path2), 'Ошибка: разное содержание у папок с одними и теми же фильтрами!'

class Test():
    """Обёртка для запуска тестов. НЕ ИСПОЛЬЗОВАТЬ ПРИ 'delete': True!!!"""
    def __init__(self):
        pass

    def start(self, inp: list):
        """Запуск тестов"""
        from program_logic import Preparer
        Preparer(inp)
        paths = {}
        print(inp)
        for p_num, params in enumerate(inp):
            print(params)
            for i, filters in enumerate(params['filters']):
                print(filters)
                paths[f'{p_num}{i}'] = [filters['actions']['output_dir']]

        print('\nТест пройден, запуск параллельной обработки...\n')
        self.__run_multiprocessing(inp, paths)
    def __run_multiprocessing(self, inp: list, paths: dict):
        """Запускает обработку тестового набора с помощью разного числа процессов. Запускает сравнение результатов обработки."""
        from program_logic import Preparer

        for i in range(1, 4):

            for p_num, params in enumerate(inp):

                if params['threads'] == i:
                    params['threads'] = i + 1
                    if i + 1 == 5:
                        params['threads'] = 1
                else:
                    params['threads'] = i

                for f_num, filters in enumerate(params['filters']):
                    filters['actions']['output_dir'] = f'{''.join(filters['actions']['output_dir'].split('-')[:-1])}-prc.{i}'
                    paths[f'{p_num}{f_num}'].append(f'{''.join(filters['actions']['output_dir'].split('-')[:-1])}-prc.{i}')
            print(paths)
            Preparer(inp)

        for paths_group in list(paths.keys()):
            for i, element in enumerate(paths_group):
                test_check_dirs(paths_group[0], paths_group[i]) # лишнее, сравнение папки под i=0 и 0 выполнять не надо