import logging

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp


logger = logging.getLogger(__name__)



def main(
    ramp_start=35,
    ramp_end=60,
    ramp_seconds=20*60,
    warn_adjustment=10,
    feel=80,
    inactive_seconds_min=10,
    inactive_seconds_max=20,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)
    with commander() as cmd:
        cmd.set_mode(Mode.CONTINUOUS)
        cmd.set_feel(feel)

        while True:
            base_level = ramp.get_value()
            warn_level = base_level - warn_adjustment

            cmd.set_level('A', warn_level)
            cmd.set_level('A', base_level)
            cmd.set_level('A', 0)

            inactive_seconds = randint(inactive_seconds_min, inactive_seconds_max)
            sleep(inactive_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()