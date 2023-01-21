from typing import Optional, Generator, Tuple, List, Dict
import hashlib
import time

from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2
from pyfingerprint.pyfingerprint import PyFingerprint

from fingerdriver.statics.status import FingerPrintDeviceStatus
from fingerdriver.statics.status import FingerPrintDeviceStatusCollection

from fingerdriver.statics.status import GeneratorStatus
from fingerdriver.statics.exceptions import FingerPrintDeviceException
from fingerdriver.models.finger import Finger

from fingerdriver.abcs.fingerdriver import FingerDeviceDriver


class PfDriver(FingerDeviceDriver):
    __BOUND_RATE: int = 57600
    __ADDRESS: int = 0xFFFFFFFF
    __DEFAULT_PASSWORD: int = 0x00000000
    __TIME_TO_SCAN_INTERVAL: int = 2

    def __init__(self, port: str, password: int = __DEFAULT_PASSWORD, scan_interval: int = __TIME_TO_SCAN_INTERVAL):
        self.__port: str = port
        self.__password: int = password
        self.__scan_interval: int = scan_interval
        self.__is_initialized: bool = False

        self.__needs_reinitialize: bool = True

        self.__BOUND_RATE: int = PfDriver.__BOUND_RATE
        self.__ADDRESS: int = PfDriver.__ADDRESS

        self.__f: Optional[PyFingerprint] = None

        self.initialize_device()

    @property
    def port(self) -> str:
        return self.__port

    @port.setter
    def port(self, port: str) -> None:
        self.__port = port

        self.__needs_reinitialize = True

    @property
    def password(self) -> int:
        return self.__password

    @password.setter
    def password(self, password: int) -> None:
        self.__password = password

        self.__needs_reinitialize = True

    @property
    def is_initialized(self) -> bool:
        return self.__is_initialized

    @property
    def scan_interval(self) -> int:
        return self.__scan_interval

    def set_password(self, old: str, new: str) -> FingerPrintDeviceStatus:
        raise NotImplemented("NotImplementedError: "
                             "this feature is not implement because it may occur destructive damage to data. "
                             f"now the password is fixed to {PfDriver.__DEFAULT_PASSWORD}.")

    def unset_password(self, password: str) -> FingerPrintDeviceStatus:
        raise NotImplemented("NotImplementedError: "
                             "this feature is not implement because it may occur destructive damage to data."
                             f"now the password is fixed to {PfDriver.__DEFAULT_PASSWORD}.")

    def initialize_device(self) -> None:
        wrong_password_error: Optional[FingerPrintDeviceStatus] = None

        try:
            self.__f = PyFingerprint(self.port, self.__BOUND_RATE, self.__ADDRESS, self.__password)

            if not self.__f.verifyPassword():
                wrong_password_error: Optional[FingerPrintDeviceStatus] = \
                    FingerPrintDeviceStatusCollection.ERROR_WRONGPASSWORD

        except Exception as e:
            if wrong_password_error is not None:
                raise FingerPrintDeviceException(wrong_password_error, None)

            unknown_error: FingerPrintDeviceStatus = FingerPrintDeviceStatusCollection.ERROR_UNKNOWN

            raise FingerPrintDeviceException(unknown_error, e)

        self.__needs_reinitialize = False

    def ensure_initialized(self) -> None:
        if self.__f is None or not self.is_initialized or self.__needs_reinitialize:
            self.initialize_device()

    def enroll_template(self, template_id: Optional[int] = 0) -> \
            Generator[Tuple[GeneratorStatus, None], Tuple[GeneratorStatus, Optional[Finger]], None]:
        self.ensure_initialized()

        yield GeneratorStatus(True, FingerPrintDeviceStatusCollection.CONTINUE_TO_NEXT_SCAN), None

        try:
            while not self.__f.readImage():
                pass

            self.__f.convertImage(FINGERPRINT_CHARBUFFER1)

            result = self.__f.searchTemplate()
            position_number: int = result[0]

            # If the finer is already registered
            if position_number >= 0:
                found: Finger = self.refer_id(position_number)
                yield GeneratorStatus(False, FingerPrintDeviceStatusCollection.ERROR_ALREADY_REGISTERED), found

            yield GeneratorStatus(True, FingerPrintDeviceStatusCollection.CONTINUE_TO_NEXT_SCAN), None
            time.sleep(2)

            while not self.__f.readImage():
                pass

            self.__f.convertImage(FINGERPRINT_CHARBUFFER2)

            # Compares the charbuffers
            if self.__f.compareCharacteristics() == 0:
                yield GeneratorStatus(False, FingerPrintDeviceStatusCollection.ERROR_NOMATCHING), None

            self.__f.createTemplate()

            position_number: int = self.__f.storeTemplate()

            registered: Finger = self.refer_id(position_number)

        except Exception as e:
            unknown_error: FingerPrintDeviceStatus = FingerPrintDeviceStatusCollection.ERROR_UNKNOWN

            raise FingerPrintDeviceException(unknown_error, e)

        yield GeneratorStatus(False, FingerPrintDeviceStatusCollection.OK), registered

    def delete_template(self, template_ids: List[int]) -> (FingerPrintDeviceStatus, List[Finger]):
        self.ensure_initialized()

        deleted_ids: List[int] = []
        deleted_fingers: List[Finger] = []

        for target_id in template_ids:
            try:
                deleting_model: Finger = self.refer_id(target_id)
                deleted_fingers.append(deleting_model)

                if self.__f.deleteTemplate(target_id):
                    pass

                else:
                    raise FingerPrintDeviceException(
                        FingerPrintDeviceStatusCollection.ERROR_DELETETEMPLATE,
                        additional_message=f"failed to delete {target_id}."
                    )

            except Exception as e:
                unknown_error: FingerPrintDeviceStatus = FingerPrintDeviceStatusCollection.ERROR_UNKNOWN
                additional_message: str = f"failed to delete {target_id}. but {deleted_ids} are already deleted."

                raise FingerPrintDeviceException(unknown_error, e, additional_message)

            deleted_ids.append(target_id)

        return FingerPrintDeviceStatusCollection.OK, deleted_fingers

    def search(self) -> Generator[Tuple[GeneratorStatus, None], Tuple[GeneratorStatus, Optional[Finger]], None]:
        self.ensure_initialized()

        yield GeneratorStatus(True, FingerPrintDeviceStatusCollection.CONTINUE_TO_NEXT_SCAN), None

        try:
            while not self.__f.readImage():
                pass

            yield GeneratorStatus(True, FingerPrintDeviceStatusCollection.CONTINUE_REMOVE_FINGER), None

            self.__f.convertImage(FINGERPRINT_CHARBUFFER1)

            result: List[int, int] = self.__f.searchTemplate()

            position_number: int = result[0]
            accuracy_score: int = result[1]

            if position_number == -1:
                yield GeneratorStatus(False, FingerPrintDeviceStatusCollection.ERROR_NOMATCHING), None

            else:
                identifier: str = self.refer_id(position_number).characteristics_identifier

                found: Finger = Finger(
                    template_id=position_number, characteristics_identifier=identifier, confidence=accuracy_score
                )

                yield GeneratorStatus(False, FingerPrintDeviceStatusCollection.OK), found

        except Exception as e:
            unknown_error: FingerPrintDeviceStatus = FingerPrintDeviceStatusCollection.ERROR_UNKNOWN

            raise FingerPrintDeviceException(unknown_error, e)

    def danger_download_image(self, path_to_save: str) -> Generator[GeneratorStatus, GeneratorStatus, None]:
        self.ensure_initialized()

        yield GeneratorStatus(True, FingerPrintDeviceStatusCollection.CONTINUE_TO_NEXT_SCAN)

        try:
            while not self.__f.readImage():
                pass

            yield GeneratorStatus(True, FingerPrintDeviceStatusCollection.CONTINUE_CREATING_IMAGE)

            self.__f.downloadImage(path_to_save)

        except Exception as e:
            unknown_error: FingerPrintDeviceStatus = FingerPrintDeviceStatusCollection.ERROR_UNKNOWN

            raise FingerPrintDeviceException(unknown_error, e)

        yield GeneratorStatus(False, FingerPrintDeviceStatusCollection.OK)

    def refer_id(self, template_id: int) -> Optional[Finger]:
        self.ensure_initialized()

        try:
            self.__f.loadTemplate(template_id, FINGERPRINT_CHARBUFFER1)

        except Exception as e:
            if str(e) == "The template could not be read":
                return None

            unknown_error = FingerPrintDeviceStatusCollection.ERROR_UNKNOWN

            raise FingerPrintDeviceException(unknown_error, e)

        characteristics = str(self.__f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)).encode('utf-8')

        hashed: str = hashlib.sha256(characteristics).hexdigest()

        found: Finger = Finger(template_id, characteristics_identifier=hashed, confidence=None)

        return found

    def get_template_count(self) -> (FingerPrintDeviceStatus, int):
        self.ensure_initialized()

        try:
            result: int = self.__f.getTemplateCount()
        except Exception as e:
            unknown_error: FingerPrintDeviceStatus = FingerPrintDeviceStatusCollection.ERROR_UNKNOWN

            raise FingerPrintDeviceException(unknown_error, e)

        return FingerPrintDeviceStatusCollection.OK, result

    def get_storage_capacity(self) -> (FingerPrintDeviceStatus, int):
        self.ensure_initialized()

        try:
            result: int = self.__f.getStorageCapacity()
        except Exception as e:
            unknown_error: FingerPrintDeviceStatus = FingerPrintDeviceStatusCollection.ERROR_UNKNOWN

            raise FingerPrintDeviceException(unknown_error, e)

        return FingerPrintDeviceStatusCollection.OK, result

    def get_template_index_table(self) -> (FingerPrintDeviceStatus, Dict[int, List[Finger]]):
        self.ensure_initialized()

        result: Dict[int, List[Finger]] = dict()

        target_id: int = 0

        try:
            for page in range(0, 3 + 1):
                table_index: List[bool] = self.__f.getTemplateIndex(page)

                result[page] = list()

                for does_template_exist_at in table_index:
                    if not does_template_exist_at:
                        target_id += 1

                        result[page].append(None)

                        continue

                    target_finger: Optional[Finger] = self.refer_id(target_id)

                    result[page].append(target_finger)

                    target_id += 1

        except Exception as e:
            unknown_error: FingerPrintDeviceStatus = FingerPrintDeviceStatusCollection.ERROR_UNKNOWN

            raise FingerPrintDeviceException(unknown_error, e)

        return FingerPrintDeviceStatusCollection.OK, result
