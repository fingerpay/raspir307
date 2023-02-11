from typing import Generator

from raspir307.statics.status import GeneratorStatus

from raspir307.impls.pyfingerprint.pf import PfDriver

if __name__ == "__main__":
    PATH_TO_SAVE: str = "/tmp/fp.bmp"

    driver: PfDriver = PfDriver(port="/dev/serial0")

    driver.ensure_initialized()

    generator: Generator[GeneratorStatus, GeneratorStatus, None] = \
        driver.danger_download_image(PATH_TO_SAVE)

    while True:
        status: GeneratorStatus = next(generator)

        print(status.status().status_description)

        if not status.should_continue():
            print(f"Your image might be saved at {PATH_TO_SAVE}")
            break
