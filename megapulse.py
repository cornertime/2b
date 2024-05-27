import logging
from oscillator import Oscillator

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp, Sequence


logger = logging.getLogger(__name__)


START = 45
RISE = 100 - START


def main(
    ramp_start=START,
    ramp_end=START + RISE,
    ramp_seconds=RISE * 60,
    feel=90,
    speed=60,
    osc_max=20,
    osc_period_seconds=90,
    step_seconds=5,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)
    osc = Oscillator(0, osc_max, osc_period_seconds)

    with commander() as cmd:
        cmd.set_power("H")
        cmd.set_mode(Mode.PULSE)
        cmd.set_speed(speed)
        cmd.set_feel(feel)

        while True:
            base_level = ramp.get_value() + osc.get_value()

            cmd.set_level("A", base_level)
            sleep(step_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
