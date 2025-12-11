from typing import Type

from django.db.models import QuerySet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from src.base.models import RegistryModel
from src.base.serializers import CallerIdSerializer


class CallerIDView(GenericAPIView):
    queryset: QuerySet[RegistryModel] = RegistryModel.objects.all()
    serializer_class:Type[CallerIdSerializer] = CallerIdSerializer
    lookup_field = None

    def get_object(self):
        phone = self.kwargs.get('phone', '')
        return RegistryModel.objects.get_data_about_phone(phone=phone)

    def get(self, request, *args, **kwargs):
        error = ''
        data = {}
        instance = self.get_object()
        if not instance:
            error = 'Нет данных по номеру'
        else:
            serializer = self.get_serializer(instance)
            data = serializer.data

        return Response({'data': data, 'error':error})


