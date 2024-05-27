import logging
from oscillator import Oscillator

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp, Sequence


logger = logging.getLogger(__name__)


START = 20
RISE = 40


def main(
    ramp_start=START,
    ramp_end=START + RISE,
    ramp_seconds=RISE * 60,
    a_adjustment=10,
    heaven_seconds_min=6,
    heaven_seconds_max=20,
    heaven_mode=Mode.WATERFALL,
    heaven_speed=90,
    heaven_feel=85,
    hell_seconds_min=10,
    hell_seconds_max=40,
    hell_adjustment=25,
    hell_speed=60,
    hell_feel=90,
    hell_mode=Mode.BOUNCE,
    inactive_seconds_min=20,
    inactive_seconds_max=40,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)

    with commander() as cmd:
        cmd.set_power("H")

        while True:
            base_level = ramp.get_value()

            cmd.set_mode(heaven_mode)
            cmd.set_feel(heaven_feel)
            cmd.set_speed(heaven_speed)
            cmd.set_level("A", base_level + a_adjustment)
            cmd.set_level("B", base_level)

            heaven_seconds = randint(heaven_seconds_min, heaven_seconds_max)
            sleep(heaven_seconds)

            cmd.set_mode(hell_mode)
            cmd.set_feel(hell_feel)
            cmd.set_speed(hell_speed)
            cmd.set_level("A", base_level + a_adjustment + hell_adjustment)
            cmd.set_level("B", base_level + hell_adjustment)

            hell_seconds = randint(hell_seconds_min, hell_seconds_max)
            sleep(hell_seconds)

            # cmd.set_level("A", 0)
            # cmd.set_level("B", 0)

            # inactive_seconds = randint(inactive_seconds_min, inactive_seconds_max)
            # sleep(inactive_seconds)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
