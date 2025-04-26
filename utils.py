import os
import random
from PIL import Image

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

    def generate_different_formats(self, path: str, num: int):
        """Создаёт в указанной папке указанное количество файлов разных форматов"""

        formats = ['xls', 'xlsx', 'png', 'jpg', 'bmp', 'ico', 'txt', 'pptx']
        seq = list('0123456789ABCDEF')

        for i in range(num):
            random.shuffle(seq)
            with open(os.path.join(path, f'{''.join(seq)}{i}.{formats[random.randint(0, 7)]}'), 'w') as file:
                file.write(f'This is a test file created by utils.py\\{self}\\{self.generate_different_formats}')

    def generate_images(self, path: str, num: int, source_path: str, format_name: str = 'Any', mode: bool = False):
        """Создаёт указанное в num количество изображений в папке path из папки source_path в формате format_name.
           Если format_name = 'Any' - псевдослучайно выбирается один из трёх форматов formats. Mode равен False по умолчанию
           и используется для рекурсивного запуска функции в случае, если кол-во изображений в source_path < num."""

        formats = ['jpg', 'bmp', 'png']
        seq = list('0123456789ABCDEF')
        if mode:
            seq.append('m')

        i = 0
        for i, file in enumerate(os.listdir(source_path)):
            if i + 1 == num: return

            random.shuffle(seq)
            img = Image.open(os.path.join(source_path, file), 'r')

            if format_name == 'Any':
                format_name = random.choice(formats)

            img.save(os.path.join(path, f'{''.join(seq)}.{format_name}'), format_name)

        if i + 1 < num:
            self.generate_images(path, num-i-1, source_path, format_name)

class CommonUtils():
    def __init__(self):
        pass

if __name__ == '__main__':
    testing_utils = TestingUtils()
    testing_utils.generate_images(r"par_tests\test_images_only", 150,
                                  source_path=r"C:\Users\filat\Downloads\Flowers.v1i.folder\train\spider lily",
                                  format_name='png')

    #testing_utils.generate_different_formats(r'par_tests\test', 200)