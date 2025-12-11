import abc
import logging

from django.db import transaction
from django.db.models import Model

from src.base.constants import UPDATE_FIELDS_REGISTRY_MODEL
from src.base.models import RegistryModel
from src.base.types import RegistryData


logger = logging.getLogger(__name__)


class AbstractPreserver(abc.ABC):

    @abc.abstractmethod
    def execute(self, data: list):
        ...


class DBRegistryPreserver(AbstractPreserver):
    data: dict[str, RegistryData] = {}
    new_objects: dict[str, RegistryModel] = {}
    updated_objects: dict[str, RegistryModel] = {}

    def execute(self, data: list[RegistryData]):
        self._prepare_data(data)
        self._split_data_to_update_and_insert_list()
        with transaction.atomic():
            if self.updated_objects:
                RegistryModel.objects.bulk_update(
                    self.updated_objects.values(),
                    UPDATE_FIELDS_REGISTRY_MODEL,
                    batch_size=100
                )
            if self.new_objects:
                try:
                    RegistryModel.objects.bulk_create(self.new_objects.values())
                except Exception as err:
                    logger.error(f"Ошибка при записи новых данных {err}")




    def _prepare_data(self, data: list[RegistryData]):
        self.data  = {item.hash: item for item in data}

    def _get_data_incoming_range(self):
        queryset = RegistryModel.objects.filter(hash__in=self.data.keys())
        return {record.hash: record for record in queryset}


    def _split_data_to_update_and_insert_list(self):
        """
        Метод разделения входных данных на список для вставки и для обновления в БД.
        Если исходить из логики типа данных предоставляемых, то меняться могут только несколько полей:
        'Оператор', 'Регион', 'Территория ГАР', 'ИНН'
        :return: None
        """
        self.new_objects = {}
        self.updated_objects = {}
        db_records = self._get_data_incoming_range()
        for hash_data, row_data in self.data.items():
            if hash_data not in db_records:
                new_obj = RegistryModel(
                    hash=row_data.hash,
                    abc_def=row_data.abc_def,
                    range_from=row_data.range_from,
                    range_to=row_data.range_to,
                    capacity=row_data.capacity,
                    operator=row_data.operator,
                    region=row_data.region,
                    territory = row_data.territory,
                    inn=row_data.inn
                )
                self.new_objects[row_data.hash] = new_obj
            else:
                db_record = db_records[hash_data]
                if (db_record.operator != row_data.operator or
                    db_record.region != row_data.region or
                    db_record.territory != row_data.territory or
                    db_record.inn != row_data.inn
                ):
                    db_record.operator = row_data.operator
                    db_record.region = row_data.region
                    db_record.territory = row_data.territory
                    db_record.inn = row_data.inn
                    self.updated_objects[db_records[hash_data]] = db_record
