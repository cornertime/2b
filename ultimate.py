import logging
from oscillator import Oscillator

from random import choice, randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp, Sequence


logger = logging.getLogger(__name__)


START = 20
RISE = 30
BASE_ADJUSTMENT = 5

adjustments = dict(
    idle=0,
    fun=BASE_ADJUSTMENT * 2,
    painful=BASE_ADJUSTMENT * 3,
    torture=BASE_ADJUSTMENT * 4,
)

periods = dict(
    idle=(10, 60),
    fun=(10, 40),
    painful=(10, 30),
    torture=(10, 20),
)

modes = list(adjustments.keys())


def main(
    ramp_start=START,
    ramp_end=START + RISE,
    ramp_seconds=RISE * 60,
    feel=90,
    speed=10,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)
    mode = "idle"

    with commander() as cmd:
        cmd.set_power("H")
        cmd.set_mode(Mode.RANDOM)
        cmd.set_speed(speed)
        cmd.set_feel(feel)

        queue = [
            ("idle", 20),
            ("fun", 20),
            ("painful", 10),
            ("torture", 10),
        ]

        while True:
            if not queue:
                new_mode = choice([m for m in modes if m != mode])
                new_seconds = randint(*periods[new_mode])
                queue.append((new_mode, new_seconds))

            mode, seconds = queue.pop(0)
            logger.info("Mode %s for %s seconds", mode, seconds)

            adjustment = adjustments[mode]
            cmd.set_level("A", ramp.get_value() + adjustment)
            sleep(seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
