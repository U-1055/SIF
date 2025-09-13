import datetime
import os
import random
import time

import filetype
from PIL import Image
from main import define_image
import re
from threading import Thread
from concurrent.futures import ProcessPoolExecutor
from natsort import natsorted
from multiprocessing import Manager


class Preparer:
    def __init__(self, parameters: list):
       # from program_interface import MessageWindow

        self.send_message('Инициализация...')
        self.t1 = datetime.datetime.now()

        params_list = []
        for parameter in parameters:
            params_list.append(self.interpret_params(parameter))

        self.image_ops(params_list)

    def interpret_params(self, parameters: dict):
        """Интерпретирует параметры, переводя их из одного словаря в три: словарь констант, фильтров и действий"""

        for param in list(parameters.keys()):

            if parameters[param] == '':
                parameters.pop(param)

            if param == 'filters':
                for i in range(len(parameters['filters'])):
                    parameters['filters'][i] = self.interpret_params(parameters['filters'][i])

            if param == 'actions':
                parameters['actions'] = self.interpret_params(parameters['actions'])

        return parameters

    def image_ops(self, params_list: list):
        """Работает с изображениями. Вызывает все необходимые для обработки функции."""

        for parameters in params_list:

            if 'total_images' in list(parameters.keys()):
                slices = parameters['total_images']
                files = natsorted(os.listdir(parameters['input_dir']))[slices[0]:slices[1]]
            else:
                files = natsorted(os.listdir(parameters['input_dir']))

            manager = Manager()
            self.loaded_images = manager.dict()
            for filters in parameters['filters']:
                self.loaded_images[filters['actions']['output_dir']] = 0

            self.dirs_files = manager.dict()
            self.inputed_in_nn = 0 #Вводится временно, для тестирования

            parameters = manager.dict(parameters)

            before = datetime.datetime.now()
            if 1 < parameters['threads']:

                self.send_message('Инициализация параллельной обработки...')
                chunk_size = len(files) // parameters['threads']
                processes = []

                with ProcessPoolExecutor() as pool:
                    chunks_size = 0 #Для тестирования

                    for i in range(parameters['threads']):
                        if i + 1 == parameters['threads']:
                            preparing_chunk = files[i * chunk_size:]
                        else:
                            preparing_chunk = files[i * chunk_size:(i + 1) * chunk_size]

                        #print(f'Размер: {len(preparing_chunk)}; Чанк: {i}')
                        chunks_size += len(preparing_chunk)
                        process = pool.submit(self.operation_cycle, (parameters, preparing_chunk, i * chunk_size))
                        processes.append(process)

                        self.send_message(f'Процесс {i + 1} запущен')

                    for process in processes:
                        self.send_message(process.result())

             #   check_chunks(parameters['input_dir'], chunks_size)
            else:
                self.send_message('Инициализация обработки...')
                before = datetime.datetime.now()
                thread = Thread(target=self.operation_cycle, args=((parameters, files, 0),)) #args дважды оборачивается в tuple по указанной в начале operation_cycle причине
                thread.start()
                thread.join()

            after = datetime.datetime.now()
            self.send_message(f'Обработка завершена: \nВремя: {after - self.t1} \nЗагружено: ')

    def operation_cycle(self, *args):
        """Выполняет операции с изображениями в одной папке. Вызывается при параллельной обработке"""

        parameters = args[0][0] #ToDo -  обратить внимание: args всегда оборачивается в tuple, из-за чего применяется [0][0] вместо [0]
        files = args[0][1]
        img_num = args[0][2]

        prepared = 0
        files_num = 0
        for file in files:
            files_num += 1
            if filetype.is_image(os.path.join(parameters['input_dir'], file)):  # проверка файла
                prepared += 1
                image = Image.open(os.path.join(parameters['input_dir'], file), 'r')

                image_params = self.get_image_params(image, parameters['input_dir'])
                image_params['number_multiplicity'] = img_num

                for i, filters in enumerate(parameters['filters']):

                    if 'prepared' in list(filters.keys()):
                        if filters['prepared'] <= self.loaded_images[filters['actions']['output_dir']]:  # <= используется для безопасности, на случай если он каким-либо образом увеличит значение
                            parameters['filters'].pop(i)

                            if len(parameters['filters']) == 0:
                                return datetime.datetime.now() - self.t1

                            continue

                    if self.check_image_compliance(image_params, filters, image):  # проверка соответствия изображения условиям
                        actions = filters['actions']

                        if actions['save']:

                            image, image_params = self.do_actions(actions, image, image_params)

                            if not os.path.exists(actions['output_dir']):
                                # Решение ниже применяется, чтобы не дать нескольким процессам одновременно создать одну папку
                                # Деление порядкового номера первого файла в чанке на общее число файлов даёт число < 0
                                if img_num != 0:
                                    time.sleep((img_num // len(files)))
                                    if not os.path.exists(actions['output_dir']):
                                        os.mkdir(actions['output_dir'])
                                else:
                                    os.mkdir(actions['output_dir'])

                            if not actions['output_dir'] in list(self.dirs_files.keys()):
                                self.dirs_files[actions['output_dir']] = os.listdir(actions['output_dir'])

                            iteration = 1
                            while f'{image_params['name']}.{image_params['extension']}' in self.dirs_files[actions['output_dir']]:  # проверка наличия идентичного имени изображения в папке
                                image_params['name'] = f'{image_params['name']}({iteration})'
                                iteration += 1

                            self.dirs_files[actions['output_dir']].append(f'{image_params['name']}.{image_params['extension']}')
                            before_load = len(os.listdir(actions['output_dir'])) # тест dirs_files

                            image.save(
                                os.path.join(actions['output_dir'],
                                             f'{image_params['name']}.{image_params['extension']}'),
                                format=image_params['format'])

                            #check_replace(actions['output_dir'], before_load) # тест dirs_files
                            image.close()

                        if actions['delete']:
                            os.remove(os.path.join(parameters['input_dir'], file))

                        self.loaded_images[filters['actions']['output_dir']] += 1
                        break
            img_num += 1

        return {'images': prepared, 'files': files_num}

    def get_image_params(self, image: Image, input_dir: str):
        """Получает параметры изображения, возвращает словарь параметров. Добавляет format, name, extension, а также параметры,
           указанные в фильтрах."""

        image_params = {}
        image_params['size'] = image.size
        image_params['weight'] = os.stat(os.path.join(input_dir, image.filename)).st_size
        image_params['name'] = ''.join(image.filename.split('\\')[-1].split('.')[0:-1])
        image_params['format'] = image.format
        image_params['extension'] = image.filename.split('\\')[-1].split('.')[-1]

        return image_params

    def check_image_compliance(self, image_params: dict, filters: dict, image: Image):
        """Проверяет соответствие изображения фильтрам путём сравнения двух словарей. Каждое условие представлено
           кортежем, который поэлементно проверяется на соответствие условию, при соответствии происходит переход к
           следующему условию (в случае, если условие нельзя проверить конструкцией if not условие in фильтр).
           Важно: в вышеуказанном случае в начале каждой итерации переменной compliance присваивается True, т.к.
           требуется, чтобы параметр соответствовал хотя бы одному из условий (что, по сути, работает как оператор or).
           Если же этого не сделать, несоответствие одного параметра будет приводить к отсеиванию изображения, независимо
           от других параметров."""

        compliance = True
        for parameter in list(filters.keys()):

            if not compliance: break

            if parameter == 'format':
                if not image_params[parameter] in filters[parameter]:
                    compliance = False

            if parameter == 'size':
                for request in filters[parameter]:
                    compliance = True
                    for i in range(2):
                        compliance = self.check_image_size(image_params[parameter][i], request[i], compliance)
                    if compliance: break # Если одно из условий группы соответствует - прервать цикл

            if parameter == 'weight':
                for request in filters[parameter]:
                    compliance = True #(!)Внимание: compliance присваивается True, т.к. требуется чтобы хотя бы одно из условий соответствовало(!)
                    compliance = self.check_image_size(image_params[parameter], request, compliance)
                    if compliance: break

            if parameter == 'name':
                for request in filters[parameter]:
                    compliance = True
                    if request[1]:  # Если True: сравнение регулярным выражением
                        if not re.match(fr'{request[0]}', image_params[parameter]):
                            compliance = False

                    if not request[1]:  # Если False: сравнение упрощённым способом
                        regex = self.create_re(request[0])

                        if not re.match(fr'{regex}', image_params[parameter]):
                            compliance = False

                    if compliance:break

            if parameter == 'extension':
                if not image_params[parameter] in filters[parameter]:
                    compliance = False

            if parameter == 'number_multiplicity':
                for request in filters[parameter]:
                    compliance = True
                    if image_params[parameter] % request != 0:
                        compliance = False

                    if compliance: break

            if parameter == 'content':
                if image_params['format'] == 'JPEG':

                    if 'content' in list(image_params.keys()):
                        if not image_params['content'] in filters[parameter]:
                            compliance = False
                    else:
                        image_params['content'] = define_image(image)[0]
                        self.inputed_in_nn += 1
                        if not image_params['content'] in filters[parameter]:
                            compliance = False
        return compliance

    def check_image_size(self, image_param: tuple, filter: tuple, compliance: bool):
        """Проверяет параметр изображения в соответствии с указанным оператором. Возвращает compliance"""

        if filter[1] == '=':
            if image_param != filter[0]:
                compliance = False

        if filter[1] == '>':
            if image_param <= filter[0]:
                compliance = False

        if filter[1] == '<':
            if image_param >= filter[0]:
                compliance = False

        return compliance

    def do_actions(self, actions: dict, image: Image, image_params: dict):
        """Выполняет указанные пользователем действия с изображением."""

        for action in list(actions.keys()):

            if action == 'resize':
                image = image.resize(actions[action])

            if action == 'rename':
                image_params['name'] = self.rename_image(image_params, actions[action], image)

            if action == 'reformat':
                image_params['format'] = actions[action]

                if image_params['format'] == 'JPEG':
                    image_params['extension'] = 'jpg'
                else:
                    image_params['extension'] = image_params['format'].lower()

            if action == 'crop':
                image = image.crop(actions[action])

        return image, image_params

    def create_re(self, request: str):
        """Формирует регулярное выражение из полученной строки. Заменяет символ * на символ *.* и
           добавляет символ ^ в начало и $ в конец"""

        if '*' in request:
            request = request.replace('*', '.*')

        return f'^{request}$'

    def rename_image(self, params: dict, img_filter: str, image: Image):
        """Переименовывает изображения по заданному шаблону. <name> - имя изображения, <total_num> - номер в входной папке,
           <сontent> - содержимое изображения, <format> - формат изображения."""

        spec_words = ['<name>', '<total_num>', '<content>', '<format>']

        for word in spec_words:

            if '<name>' in img_filter:
                img_filter = img_filter.replace(word, params['name'])
            if '<total_num>' in img_filter:
                img_filter = img_filter.replace(word, str(params['number_multiplicity']))
            if '<format>' in img_filter:
                img_filter = img_filter.replace(word, params['format'])

            if '<content>' in img_filter:

                if 'content' in params:
                    img_filter = img_filter.replace(word, str(params['content']))
                else:
                    img_filter = img_filter.replace(word, define_image(image)[0])

        return img_filter

    def send_stat(self):
        pass

    def update_progress(self, all_images: int, prepared: int):
        #ToDo: разобраться с импортами

        self.send_message('Ошибка обновления прогресса', 'error')

    def send_message(self, message: str, type: str = 'message'):
        """Передаёт сообщение в интерфейс. Types: message, warning, error, fatal error."""
        pass
       # self.msg_window.print_message(message)

if __name__ == '__main__':
    errors = 0
    for i in range(1):
            print(f'{i}:')
            Preparer([{'input_dir': r'C:\Users\filat\OneDrive\Документы\Проект\target_dir', 'total_images': (0, 10), 'threads': 1,
                   'filters': #-----------------------------------------------------------------------------------------
                         [
                          {'format': 'JPEG',
                            'size': (((10, '>'), (10, '>')),),
                            'weight': ((10, '>'),),
                            'name': (('s*sss', True),),
                            'extension': 'jpeg',
                            'number_multiplicity': (1, 2, 3, 4, 5),
                            'content': 'I',
                            'prepared': '',
                            'actions':  # -----------------------------------------------------------------------------------
                                {'resize': (110, 100),
                                 'crop': (110, 25, 24, 12),
                                 'reformat': 'PNG',
                                 'rename': f'{random.randint(100, 315)}<total_num>-jpg',
                                 'save': True,
                                 'delete': False,
                                 'output_dir': r'C:\Users\filat\OneDrive\Документы\Проект\target_dir'}}
                                           ]}])

