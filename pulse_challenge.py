import logging
from oscillator import Oscillator

from random import randint
from time import sleep

from estim_2b import Mode, commander


logger = logging.getLogger(__name__)


def main(
    ramp_start=50,
    ramp_end=100,
    feel=80,
    speed=30,
    active_seconds=5,
    inactive_seconds=10,
):
    with commander() as cmd:
        cmd.set_power("H")
        cmd.set_mode(Mode.PULSE)
        cmd.set_feel(feel)
        cmd.set_speed(speed)

        for base_level in range(ramp_start, ramp_end + 1):
            cmd.set_level("A", base_level)
            sleep(active_seconds)
            cmd.set_level("A", 0)

            sleep(inactive_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
