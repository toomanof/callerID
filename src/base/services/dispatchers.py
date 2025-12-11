import abc
from typing import Type, Optional

from src.base.services.downloaders import AbstractDownloader, RegistryCSVDownloader
from src.base.services.preservers import AbstractPreserver, DBRegistryPreserver


class AbstractDispatcher(abc.ABC):

    @abc.abstractmethod
    def execute(self, **kwargs):
        ...

    @abc.abstractmethod
    def fetch_data(self):
        ...

    @abc.abstractmethod
    def save_data(self):
        ...


class BaseDispatcher(AbstractDispatcher):
    class_downloader: Type[AbstractDownloader]
    class_preserver: Type[AbstractPreserver]
    downloader: Optional[AbstractDownloader] = None
    preserver: Optional[AbstractPreserver] = None
    data: list = []


    def __init__(self):
        self.preserver = self.class_preserver()

    def execute(self, url: str):
        self.downloader = self.class_downloader(url=url)
        self.fetch_data()
        self.save_data()

    def fetch_data(self):
        self.data =  self.downloader.execute()

    def save_data(self):
        if self.data:
            self.preserver.execute(self.data)


class RegistryDispatcher(BaseDispatcher):
    class_downloader = RegistryCSVDownloader
    class_preserver = DBRegistryPreserver
