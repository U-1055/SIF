import os


class FileUtils():
    def __init__(self):
        pass

    def get_difference(self, list_1: list or tuple, list_2: list or tuple):
        """Находит разницу между двумя списками: возвращает список элементов, которые есть в 1-м списке но отсутствуют в другом"""
        pass


    def unpack(self, path, output_path):
        """Перемещает все файлы из директорий по указанному пути"""
        #Работает ТОЛЬКО для директорий, ПОЛНОСТЬЮ заполненных директориями
        for file in os.listdir(path):

            for sub_file in os.listdir(os.path.join(path, file)):
                pass#ToDo:


class TestingUtils():
    def __init__(self):
        pass

    def write_result(self, path: str, test_name: str, description: str, input: dict, time: str):
        """Записывает результаты тестового запуска программы в выходную директорию."""

        with open(path, 'w') as file:
            file.write(f'Test: {test_name}\nDescription: {description}\nTime: {time}\nInput: {input}')

class CommonUtils():
    def __init__(self):
        pass

