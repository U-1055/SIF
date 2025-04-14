"""Тесты логики"""
import os


def check_chunks(path: str, chunks: int):
    """Проверка соответствия количества изображений в чанках количеству изображений во входной папке"""

    in_dir = len(os.listdir(path))
    assert in_dir == chunks, (f'Разное количество изображений в папке и в чанках, в папке: {in_dir}; в чанках: {chunks};]\n')