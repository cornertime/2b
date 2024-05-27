import logging
from oscillator import Oscillator

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp, Sequence


logger = logging.getLogger(__name__)


START = 55
RISE = 100 - START

MIN_SPEED = 20
MAX_SPEED = 85


def main(
    ramp_start=START,
    ramp_end=START + RISE,
    ramp_seconds=RISE * 60,
    feel=90,
    active_seconds_min=2,
    active_seconds_max=6,
    inactive_seconds_min=10,
    inactive_seconds_max=40,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)

    with commander() as cmd:
        cmd.set_power("H")
        cmd.set_mode(Mode.PULSE)
        cmd.set_feel(feel)

        while True:
            speed = randint(MIN_SPEED, MAX_SPEED)
            cmd.set_speed(speed)

            active_seconds = randint(active_seconds_min, active_seconds_max)
            cmd.set_level("A", ramp.get_value())
            sleep(active_seconds)

            inactive_seconds = randint(inactive_seconds_min, inactive_seconds_max)
            cmd.set_level("A", 0)
            sleep(inactive_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
