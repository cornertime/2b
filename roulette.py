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
    warn_adjustment=2,
    feel=80,
    warn_seconds=3,
    bang_adjustment_min=10,
    bang_adjustment_max=20,
    active_seconds=1,
    inactive_seconds_min=10,
    inactive_seconds_max=30,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)
    seq = Sequence()
    time_osc = Oscillator(inactive_seconds_min, inactive_seconds_max, 120)
    bang_adjustment = bang_adjustment_min

    with commander() as cmd:
        cmd.set_mode(Mode.CONTINUOUS)
        cmd.set_power("H")
        cmd.set_feel(feel)

        while True:
            active_level = ramp.get_value()
            warn_level = active_level // warn_adjustment

            if randint(1, 6) == 1:
                # bang
                active_level += bang_adjustment
                bang_adjustment = min(bang_adjustment + 1, bang_adjustment_max)

            cmd.set_level("A", warn_level)
            sleep(warn_seconds)
            cmd.set_level("A", active_level)
            sleep(active_seconds)
            cmd.set_level("A", 0)

            # inactive_seconds = randint(inactive_seconds_min, inactive_seconds_max)
            inactive_seconds = time_osc.get_value()
            sleep(inactive_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
