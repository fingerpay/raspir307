from typing import Optional, Union, Generator, Tuple, List, Dict

from abc import ABCMeta, abstractmethod

from raspir307.statics.status import FingerPrintDeviceStatus
from raspir307.statics.status import GeneratorStatus
from raspir307.models.finger import Finger


class FingerDeviceDriver(metaclass=ABCMeta):
    @property
    @abstractmethod
    def port(self) -> str:
        pass

    @port.setter
    @abstractmethod
    def port(self, port: str) -> None:
        pass

    @property
    @abstractmethod
    def password(self) -> int:
        pass

    @password.setter
    @abstractmethod
    def password(self, password: int) -> None:
        pass

    @property
    @abstractmethod
    def is_initialized(self) -> bool:
        pass

    @property
    @abstractmethod
    def scan_interval(self) -> int:
        pass

    @abstractmethod
    def set_password(self, old: int, new: int) -> FingerPrintDeviceStatus:
        pass

    @abstractmethod
    def unset_password(self, password: int) -> FingerPrintDeviceStatus:
        pass

    @abstractmethod
    def initialize_device(self) -> None:
        pass

    @abstractmethod
    def ensure_initialized(self) -> None:
        pass

    @abstractmethod
    def enroll_template(self, template_id: Optional[int] = 0) -> \
            Generator[
                Tuple[GeneratorStatus, None], Tuple[GeneratorStatus, None], Tuple[GeneratorStatus, Optional[Finger]]
            ]:
        pass

    @abstractmethod
    def delete_template(self, template_ids: List[int]) -> (FingerPrintDeviceStatus, List[Finger]):
        pass

    @abstractmethod
    def search(self) -> Generator[Tuple[GeneratorStatus, None], Tuple[GeneratorStatus, Optional[Finger]], None]:
        pass

    @abstractmethod
    def danger_download_image(self, path_to_save: str) -> Generator[GeneratorStatus, GeneratorStatus, None]:
        pass

    @abstractmethod
    def refer_id(self, template_id: int) -> (FingerPrintDeviceStatus, Optional[Finger]):
        pass

    @abstractmethod
    def get_template_count(self) -> (FingerPrintDeviceStatus, int):
        pass

    @abstractmethod
    def get_storage_capacity(self) -> (FingerPrintDeviceStatus, int):
        pass

    @abstractmethod
    def get_template_index_table(self) -> (
            FingerPrintDeviceStatus, Union[Dict[int, List[Optional[Finger]]], List[Optional[Finger]]]):
        pass
