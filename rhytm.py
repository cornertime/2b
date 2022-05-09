import logging

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp


logger = logging.getLogger(__name__)



def main(
    ramp_start=40,
    ramp_end=60,
    ramp_seconds=20*60,
    short_ramp_rounds=20,
    short_ramp_multiplier=2,
    speed=40,
    feel=80,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)
    with commander() as cmd:
        cmd.set_mode(Mode.PULSE)
        cmd.set_feel(feel)
        cmd.set_speed(speed)

        while True:
            base_value = ramp.get_value()

            for short_ramp_adjustment in range(short_ramp_rounds):
                cmd.set_level('A', base_value + short_ramp_adjustment * short_ramp_multiplier)
                cmd.set_level('A', 0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()