from django.db import models


class RegistryManager(models.Manager):

    def get_data_about_phone(self, phone: str):
        if not phone or len(phone) < 11:
            return self.get_queryset().none()

        code = phone[1:4]
        number = phone[4:]
        return self.get_queryset().filter(
            abc_def=code,
            range_from__lte=number,
            range_to__gte=number
        ).first()


class RegistryModel(models.Model):
    hash = models.CharField(max_length=500, primary_key=True)
    abc_def = models.PositiveIntegerField('Код')
    range_from = models.PositiveIntegerField('Диапозон от', db_index=True)
    range_to = models.PositiveIntegerField('Диапозон до', db_index=True)
    capacity =models.PositiveIntegerField('Емкость')
    operator = models.CharField('Оператор', max_length=255)
    region = models.CharField('Регион', max_length=255)
    territory = models.CharField('Территория ГАР', max_length=255)
    inn = models.CharField('INN', max_length=255)

    objects = RegistryManager()

    class Meta:
        indexes = [
            models.Index(fields=['abc_def', 'range_from', 'range_to'])
        ]