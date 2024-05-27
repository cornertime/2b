import logging
from oscillator import Oscillator

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp, Sequence


logger = logging.getLogger(__name__)


START = 35
RISE = 100 - START


def main(
    ramp_start=START,
    ramp_end=START + RISE,
    ramp_seconds=RISE * 60,
    speed=5,
    feel=90,
    inactive_level=25,
    active_seconds_min=5,
    active_seconds_max=10,
    inactive_seconds_min=10,
    inactive_seconds_max=40,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)

    with commander() as cmd:
        cmd.set_power("H")
        cmd.set_mode(Mode.RANDOM)
        cmd.set_speed(speed)
        cmd.set_feel(feel)

        while True:
            active_seconds = randint(active_seconds_min, active_seconds_max)
            cmd.set_level("A", ramp.get_value())
            sleep(active_seconds)

            inactive_seconds = randint(inactive_seconds_min, inactive_seconds_max)
            cmd.set_level("A", inactive_level)
            sleep(inactive_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
