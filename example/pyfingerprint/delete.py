from typing import Tuple, List

from raspir307.statics.status import FingerPrintDeviceStatus
from raspir307.models.finger import Finger

from raspir307.impls.pyfingerprint.pf import PfDriver

if __name__ == "__main__":
    driver: PfDriver = PfDriver(port="/dev/serial0")

    driver.ensure_initialized()

    id_to_delete: int = int(input("Template ID to delete?\n"))

    result: Tuple[FingerPrintDeviceStatus, List[Finger]] = driver.delete_template([id_to_delete])

    print(f"Deleted: {result[1]}")
