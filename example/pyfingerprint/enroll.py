from typing import Optional, Generator, Tuple

from raspir307.statics.status import GeneratorStatus
from raspir307.models.finger import Finger

from raspir307.impls.pyfingerprint.pf import PfDriver

if __name__ == "__main__":
    driver: PfDriver = PfDriver(port="/dev/serial0")

    driver.ensure_initialized()

    generator: Generator[Tuple[GeneratorStatus, None], Tuple[GeneratorStatus, Optional[Finger]], None] = \
        driver.enroll_template()

    while True:
        status: Tuple[GeneratorStatus, Optional[Finger]] = next(generator)

        print(status[0].status().status_description)

        if status[1] is not None:
            print(status[1].template_id, status[1].characteristics_identifier, status[1].confidence)

        if not status[0].should_continue():
            break
