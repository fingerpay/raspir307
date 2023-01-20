from typing import Optional


class FingerPrintDeviceStatus:
    def __init__(self, status_code: int, status_name: str, is_error: bool, status_description: str, ):
        self.__status_code: int = status_code
        self.__status_name: str = status_name
        self.__is_error: bool = is_error
        self.__status_description: str = status_description

    @property
    def status_code(self) -> int:
        return self.__status_code

    @property
    def status_name(self) -> str:
        return self.__status_name

    @property
    def status_description(self) -> str:
        return self.__status_description

    @property
    def is_error(self) -> bool:
        return self.__is_error


class FingerPrintDeviceStatusCollection:
    # OK

    OK: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x00, "OK", False,
        "OK"
    )

    # Continue

    CONTINUE_TO_NEXT_SCAN: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x101, "TO_NEXT_SCAN_CONTINUE", False,
        "Waiting for next finger scan. Please call next."
    )

    CONTINUE_CREATING_IMAGE: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x102, "CREATING_IMAGE_CONTINUE", False,
        "Creating the image... Please call next and wait a second."
    )

    CONTINUE_REMOVE_FINGER: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x103, "REMOVE_FINGER_CONTINUE", False,
        "Please remove the finger and call next."
    )

    # Errors

    ERROR_COMMUNICATION: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x01, "COMMUNICATION_ERROR", True,
        "Failed to communicate with the device."
    )

    ERROR_WRONGPASSWORD: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x13, "WRONGPASSWORD_ERROR", True,
        "The password is wrong!"
    )

    ERROR_INVALIDREGISTER: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x1A, "INVALIDREGISTER_ERROR", True,
        "The registration is invalid."
    )

    ERROR_NOFINGER: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x02, "NOFINGER_ERROR", True,
        "No finger detected."
    )

    ERROR_READIMAGE: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x03, "READIMAGE_ERROR", True,
        "Failed to read the image."
    )

    ERROR_MESSYIMAGE: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x06, "MESSYIMAGE_ERROR", True,
        "The image is to messy. Please consider to clean up the device sensor."
    )

    ERROR_FEWFEATUREPOINTS: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x07, "FEWFEATUREPOINT_ERROR", True,
        "The feature points of the image is too few to recognize. Please touch the sensor firmly."
    )

    ERROR_INVALIDIMAGE: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x15, "INVALIDIMAGE_ERROR", True,
        "The image is invalid."
    )

    ERROR_CHARACTERISTICSMISMATCH: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x0A, "CHARACTERISTICSMISMATCH_ERROR", True,
        "The characteristics of the image is match."
    )

    ERROR_INVALIDPOSITION: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x0B, "INVALIDPOSITION_ERROR", True,
        "You are trying to store template in invalid address."
    )

    ERROR_FLASH: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x18, "FLASH_ERROR", True,
        "Already flashed."
    )

    ERROR_NOTEMPLATEFOUND: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x09, "NOTEMPLATEFOUND_ERROR", True,
        "No matching template found."
    )

    ERROR_LOADTEMPLATE: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x0C, "LOADTEMPLATE_ERROR", True,
        "Failed to load the template."
    )

    ERROR_DELETETEMPLATE: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x10, "DELETETEMPLATE_ERROR", True,
        "Failed to delete the template."
    )

    ERROR_CLEARDATABASE: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x11, "CLEARDATABASE_ERROR", True,
        "Failed to clear the database."
    )

    ERROR_NOMATCHING: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x08, "NOMATCHING_ERROR", True,
        "No matching found."
    )

    ERROR_DOWNLOADIMAGE: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x0F, "DOWNLOADIMAGE_ERROR", True,
        "Failed to download image."
    )

    ERROR_DOWNLOADCHARACTERISTICS: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0x0D, "DOWNLOADCHARACTERISTICS_ERROR", True,
        "Failed to download the characteristics."
    )

    ERROR_TIMEOUT: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0xFF, "TIMEOUT_ERROR", True,
        "Timeout."
    )

    ERROR_BADPACKET: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0xFE, "BADPACKET_ERROR", True,
        "Received bad packet."
    )

    ERROR_UNKNOWN: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0xFFFF, "UNKNOWN_ERROR", True,
        "Unknown error."
    )

    ERROR_ALREADY_REGISTERED: FingerPrintDeviceStatus = FingerPrintDeviceStatus(
        0xFFF0, "ALREADY_REGISTERED_ERROR", True,
        "This fingerprint is already registered."
    )


class GeneratorStatus:
    def __init__(self, should_go_next: bool, status: Optional[FingerPrintDeviceStatus] = None):
        self.__should_continue: bool = should_go_next
        self.__status: Optional[FingerPrintDeviceStatus] = status

    def should_continue(self) -> bool:
        return self.__should_continue

    def status(self) -> Optional[FingerPrintDeviceStatus]:
        return self.__status
