import logging
from oscillator import Oscillator

from random import randint
from time import sleep

from estim_2b import Mode, commander


logger = logging.getLogger(__name__)

def main(
    ramp_start=25,
    ramp_end=100,
    warn_adjustment=2,
    feel=80,
    warn_seconds=3,
    active_seconds=1,
    inactive_seconds=10,
):
    with commander() as cmd:
        cmd.set_power('H')
        cmd.set_mode(Mode.CONTINUOUS)
        cmd.set_feel(feel)

        for base_level in range(ramp_start, ramp_end + 1):
            warn_level = base_level // warn_adjustment

            cmd.set_level('A', warn_level)
            sleep(warn_seconds)
            cmd.set_level('A', base_level)
            sleep(active_seconds)
            cmd.set_level('A', 0)

            sleep(inactive_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
