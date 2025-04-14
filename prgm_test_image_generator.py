"""Содержит код для генерации изображений из каталога test, а также тесты программы"""
import os
import random
from utils import FileUtils

import filetype
from PIL import Image
import re
from natsort import natsorted
from openpyxl import Workbook

letters_data = {
    '0': 'A',  '6': 'G',   '12': 'M',  '18': 'S',  '24': 'Y',
    '1': 'B',  '7': 'H',   '13': 'N',  '19': 'T',  '25': 'Z',
    '2': 'C',  '8': 'I',   '14': 'O',  '20': 'U',  '26': 'Не удалось распознать букву',
    '3': 'D',  '9': 'J',   '15': 'P',  '21': 'V',
    '4': 'E',  '10': 'K',  '16': 'Q',  '22': 'W',
    '5': 'F',  '11': 'L',  '17': 'R',  '23': 'X',
}

def generate():

    train_path = 'Letters.v1i.multiclass\\train'

    with open(os.path.join(train_path, '_classes.csv'), 'r') as lbl:
        vals = lbl.readlines()

    vals = vals[1:]
    values = {}

    for line in vals:

        for i, num in enumerate(line.split(',')[1::]):
            if '1' in num:
                values[line.split(',')[0].strip()] = letters_data[str(i)]
    i = 0
    images = 0
    save_dir = '10k.jpeg'
    os.mkdir(os.path.join('test_dirs', save_dir))
    formats = {'JPEG': 'jpg', 'PNG': 'png', 'BMP': 'bmp'}

    for file in os.listdir(train_path):
        if i != 0 and i % 2000 == 0:
            images = 0

        if file != '_classes.csv':

            image = Image.open(os.path.join(train_path, file), 'r')
            name = image.filename.split('\\')[-1]

            resizes = [(150, 150), (150, 75), (75, 150), (75, 75)]

            key = 'JPEG'

            image.save(os.path.join('test_dirs', save_dir, f'_{i}.{formats[key]}'), format=key)
            image.close()
            images += 1
            i += 1
class Test():
    def __init__(self):
        pass

    def create_stat(self, files: list, path: str, output: str):

        wb = Workbook()
        table = wb.active

        table['A1'] = 'Имя файла'
        table['B1'] = 'Формат'
        table['C1'] = 'Расширение файла'
        table['D1'] = 'Размер'
        table['E1'] = 'Разрешение (ширина)'
        table['F1'] = 'Разрешение (высота)'
        table['G1'] = 'Номер'
        table['H1'] = 'Содержимое'

        for i, file in enumerate(files):
            if filetype.is_image(os.path.join(path, file)):
                image = Image.open(os.path.join(path, file), 'r')

                table[f'A{i + 2}'] = ''.join(image.filename.split('\\')[-1])
                table[f'B{i + 2}'] = image.format
                table[f'C{i + 2}'] = image.filename.split('\\')[-1].split('.')[-1]
                table[f'D{i + 2}'] = os.stat(os.path.join(path, image.filename)).st_size
                table[f'E{i + 2}'] = image.size[0]
                table[f'F{i + 2}'] = image.size[1]
                table[f'G{i + 2}'] = i
                table[f'H{i + 2}'] = file.split('_')[0]

                image.close()

        wb.save(output)

    def get_size_data(self, path, request):

        number = 0
        for file in os.listdir(path):
            image = Image.open(os.path.join(path, file), 'r')

            if image.size == request:
                number += 1

        return number

    def get_set_data(self, path):

        images = len(os.listdir(path))

        formats = {}
        extensions = {}
        sizes = []
        weights = []
        for file in os.listdir(path):
            image = Image.open(os.path.join(path, file))
            if not image.format in list(formats.keys()):
                formats[image.format] = 0

            if not file.split('.')[-1] in extensions:
                extensions[file.split('.')[-1]] = 0
            extensions[file.split('.')[-1]] += 1

            formats[image.format] += 1
            sizes.append(image.size)
            weights.append(os.stat(os.path.join(path, file)).st_size)

        total_weight = 0
        for val in weights:
            total_weight += val

        median_weight = total_weight // images

        max_ext_idx = 0
        sum_list = []
        for val in sizes:
            sum_list.append(val[0] + val[1])

        max_ext_idx = sum_list.index(max(sum_list))
        min_ext_idx = sum_list.index(min(sum_list))

        print(f'Информация о наборе изображений {path}:\nКоличество изображений: {images}\nФорматы файлов: {formats}\nРасширения файлов: {extensions}\n'
              f'Макс. размер файла: {max(weights)} | Мин. размер файла: {min(weights)}\nСредний размер файла: {median_weight}\nМакс. разрешение: {sizes[max_ext_idx]}'
              f'| Мин. разрешение: {sizes[min_ext_idx]} ')

    def nn_test(self, request: list, files, output_path: str, ext: str):
        """Тестирует фильтр по содержанию, проверяя количество верно определённых изображений. Выводит процентную точность фильтра."""
        currents = 0

        for file in os.listdir(output_path):
            if file.split('_')[0] in request:
                currents += 1

        input_currents = 0
        print(files)
        for file in files:
            if file.split('_')[0] in request and file.split('.')[-1] == ext:
                input_currents += 1

        if currents == input_currents:
            print(f'\nТест нейронной сети пройден - результат: \nВерно определено: {(currents / len(os.listdir(output_path))) * 100}% \n')
        else:
            print(f'\nОпределены не все изображения - определено: \nВо входной папке: {input_currents}; В выходной: {currents}\n Точность: {(currents / len(os.listdir(output_path))) * 100}%')

    def common_test(self, parameters: dict, path: str):
        """Тестирует некоторые базовые фильтры"""
        check_val = parameters['load_images']
        if parameters['load_images'] == '' or parameters['load_images'] > parameters['total_images']:
            check_val = parameters['total_images']

        if parameters['total_images'] == '':
            check_val = ''

        for i, file in enumerate(os.listdir(path)):
            if check_val != '':
                if i + 1 == check_val:
                    return 'Ошибка: в выходной папке больше изображений, чем требует запрос'

    def search_test(self, request: str, input_dir: str, output_dir):

        currents = 0
        for file in os.listdir(input_dir):
            if re.match(fr'{request}', file.split('.')[0]):
                currents += 1

        output_currents = 0
        output_mistakes = 0

        for file in os.listdir(output_dir):
            if re.match(fr'{request}', file.split('.')[0]):
                output_currents += 1
            else:
                output_mistakes += 1

        if currents == output_currents and output_mistakes == 0:
            print(f'Тест пройден, ошибки отсутствуют: ')
        else:
            print(f'Тест не пройден, ошибки: output:{output_mistakes}, совпадений в входной папке: {currents}, совпадений в выходной папке: {output_currents}')

def test_interface():
    """Интерфейс для тестов"""
    for i in range(1):
        pass

if __name__ == '__main__':
    generate()