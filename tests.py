"""Тесты логики"""
import os


def check_chunks(path: str, chunks: int):
    """Проверка соответствия количества изображений в чанках количеству изображений во входной папке"""

    in_dir = len(os.listdir(path))
    assert in_dir == chunks, (f'Разное количество изображений в папке и в чанках, в папке: {in_dir}; в чанках: {chunks};]\n')

def check_replace(path: str, last_num: int):
    """Проверяет, не было ли изображение в папке заменено выгружаемым путём сравнения предыдущего числа файлов в папке и текущего
       (разница должна быть равна 1)."""
    print('last_num:', last_num)
    print('len:', len(os.listdir(path)))
    assert len(os.listdir(path)) - 1 == last_num, 'Ошибка: выгруженное изображение заменило изображение в папке!'