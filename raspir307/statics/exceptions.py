from typing import Optional

import traceback

from raspir307.statics.status import FingerPrintDeviceStatus


class FingerPrintDeviceException(BaseException):
    def __init__(self, status: Optional[FingerPrintDeviceStatus] = None,
                 context: Optional[Exception] = None, additional_message: str = "", **kwargs):
        super().__init__(kwargs)

        self.__status: Optional[FingerPrintDeviceStatus] = status
        self.__additional_message: str = additional_message
        self.__context: Optional[Exception] = context

    @property
    def status(self) -> Optional[FingerPrintDeviceStatus]:
        return self.__status

    @property
    def context(self) -> Optional[Exception]:
        return self.__context

    def __get_context_traceback(self) -> str:
        try:
            raise self.context

        except Exception:
            return traceback.format_exc()

    def __str__(self) -> str:
        if isinstance(self.status, FingerPrintDeviceStatus):
            message = f"FingerPrintDeviceError: " \
                      f"{self.status.status_description} ({self.status.status_name} {self.status.status_code})"

        else:
            message = "UnknownFingerPrintDeviceError: an unknown error occurred in the fingerprint device"

        if self.__additional_message:
            message += f"\n" \
                       f"\n" \
                       f"Additional Message: {self.__additional_message}"

        if self.context:
            message += f"\n" \
                       f"\n" \
                       f"Context:\n" \
                       f"\n" \
                       f"{self.__get_context_traceback()}"

        return message
