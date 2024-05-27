import logging
from oscillator import Oscillator

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp, Sequence


logger = logging.getLogger(__name__)


START = 40
RISE = 100 - START


def main(
    ramp_start=START,
    ramp_end=START + RISE,
    ramp_seconds=RISE * 60,
    speed=40,
    feel=90,
    a_adjustment=20,
    active_seconds_min=5,
    active_seconds_max=10,
    inactive_seconds_min=10,
    inactive_seconds_max=30,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)

    with commander() as cmd:
        cmd.set_power("H")
        cmd.set_mode(Mode.BOUNCE)
        cmd.set_speed(speed)
        cmd.set_feel(feel)

        while True:
            base_level = ramp.get_value()
            cmd.set_level("B", base_level)
            active_seconds = randint(active_seconds_min, active_seconds_max)
            cmd.set_level("A", base_level + a_adjustment)
            sleep(active_seconds)

            inactive_seconds = randint(inactive_seconds_min, inactive_seconds_max)
            cmd.set_level("A", 0)
            sleep(inactive_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
