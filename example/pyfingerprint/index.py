from typing import Tuple, List, Dict

from raspir307.statics.status import FingerPrintDeviceStatus
from raspir307.models.finger import Finger

from raspir307.impls.pyfingerprint.pf import PfDriver

if __name__ == "__main__":
    print("This operation may take time. Hold tight...")

    driver: PfDriver = PfDriver(port="/dev/serial0")

    driver.ensure_initialized()

    result: Tuple[FingerPrintDeviceStatus, Dict[int, List[Finger]]] = driver.get_template_index_table()

    status: FingerPrintDeviceStatus = result[0]
    table: Dict[int, List[Finger]] = result[1]

    print("Result:\n")

    for page in table.keys():
        print(f"Page {page}\n")

        for finger in table[page]:
            print(finger)
