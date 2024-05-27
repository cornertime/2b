import logging
from oscillator import Oscillator

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp, Sequence


logger = logging.getLogger(__name__)

START = 25
RISE = 40


def main(
    ramp_start=START,
    ramp_end=START + RISE,
    ramp_seconds=RISE * 90,
    b_adjustment=15,
    warn_adjustment=2,
    feel=90,
    warn_seconds=1,
    osc_multiplier=2,
    active_seconds=0,
    inactive_seconds_min=10,
    inactive_seconds_max=30,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)
    seq = Sequence()
    time_osc = Oscillator(inactive_seconds_min, inactive_seconds_max, 120)

    with commander() as cmd:
        cmd.set_power("H")
        cmd.set_mode(Mode.A_SPLIT)
        cmd.set_feel(feel)

        while True:
            base_level = ramp.get_value() + osc_multiplier * seq.get_value()
            warn_level = base_level // warn_adjustment

            cmd.set_level("B", base_level + b_adjustment)
            cmd.set_level("A", warn_level)
            sleep(warn_seconds)
            cmd.set_level("A", base_level)
            sleep(active_seconds)
            cmd.set_level("A", 0)

            # inactive_seconds = randint(inactive_seconds_min, inactive_seconds_max)
            inactive_seconds = time_osc.get_value()
            sleep(inactive_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
