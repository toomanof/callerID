import abc
import csv
import hashlib
import logging
from typing import Optional

import requests
import tempfile

from dataclasses import dataclass

from requests import RequestException

from src.base.constants import KEYS_CSV, HEAD_REQUEST, FIELD_FOR_HASH
from src.base.types import RegistryData

logger = logging.getLogger(__name__)


class AbstractDownloader(abc.ABC):

    def __init__(self, **kwargs):
        ...

    @abc.abstractmethod
    def execute(self) ->list:
        """
        Метод получения загруженных значений
        :return: Список значений
        """
        ...


@dataclass
class RegistryCSVDownloader(AbstractDownloader):
    url: str

    def execute(self) -> list[RegistryData]:
        """
        Метод получения загруженных значений
        :return: Список значений
        """
        result = []
        path_csv_file = self._fetch_csv()
        if path_csv_file:
            result = self._csv_to_list(path_csv_file)
        return result

    def _fetch_csv(self) -> Optional[str]:
        """
        Метод загрузки csv файла во временный файл
        :return: Путь к временному файлу
        """
        result = None
        with requests.get(url=self.url, headers=HEAD_REQUEST, stream=True, timeout=30) as response:
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                    logger.info(f'Загружен файл: {tmp.name}')
                    for chunk in response.iter_content(chunk_size=128):
                        tmp.write(chunk)
                    result = tmp.name
            else:
                logger.error(f'Во время попытки загрузки csv файла произошла ошибка. Error:{response.status_code}. URL: {self.url}')
        return result

    @staticmethod
    def _prepare_keys(data: dict) -> dict:
        """
        Преобразование ключей в латинский вид
        :param data: словарь с кирилличными ключами
        :return: словарь с новыми ключами
        """
        result = {}
        for key, val in data.items():
            try:
                new_key = KEYS_CSV[key]
            except KeyError:
                logger.error(f'Не найден ключ в словаре. {key=}. {data=}')
                continue
            result[new_key] = val
        return result

    @staticmethod
    def _dict_to_registry_data(data: dict) -> RegistryData:
        seq_filed_for_hash = (data.get(field, '') for field in FIELD_FOR_HASH)
        val_str = ','.join(seq_filed_for_hash)
        hash_val = hashlib.sha256(val_str.encode())
        data['hash'] = hash_val.hexdigest()
        return RegistryData(**data)


    def _csv_to_list(self, path_csv_file: str) -> list[RegistryData]:
        """
        Чтение данных с csv файла и преобразование их в список
        :param path_csv_file: имя csv файлаа
        :return: Список данных с csv файла
        """
        result = []
        errors = []
        try:
            with open(path_csv_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter=';')
                for row_num, row in enumerate(reader, start=2):
                    try:
                        data = self._dict_to_registry_data(self._prepare_keys(row))
                        result.append(data)
                    except Exception as err:
                        errors.append(f'Строка {row_num}: ошибка обработки данных: {err}')

        except FileNotFoundError:
            logger.error(f'Файл не найден: {path_csv_file}')
        except Exception as err:
            logger.error(f'Ошибка чтения файла: {err}')

        if errors:
            logger.error('Ошибки при чтении CSV:')
            for error in errors:
                logger.error(error)
        return result

