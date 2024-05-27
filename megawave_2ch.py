import logging
from oscillator import Oscillator

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp, Sequence


logger = logging.getLogger(__name__)

START = 15
RISE = 40


def main(
    ramp_start=START,
    ramp_end=START + RISE,
    ramp_seconds=RISE * 60,
    feel=90,
    speed=5,
    a_adjustment=5,
    osc_a_max=10,
    osc_a_period_seconds=113,
    osc_b_max=10,
    osc_b_period_seconds=127,
    step_seconds=5,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)
    osc_a = Oscillator(0, osc_a_max, osc_a_period_seconds)
    osc_b = Oscillator(0, osc_b_max, osc_b_period_seconds)

    with commander() as cmd:
        cmd.set_power("H")
        cmd.set_mode(Mode.WAVE)
        cmd.set_speed(speed)
        cmd.set_feel(feel)

        while True:
            base_level = ramp.get_value()
            a_level = base_level + osc_a.get_value() + a_adjustment
            b_level = base_level + osc_b.get_value()

            cmd.set_level("B", b_level)
            cmd.set_level("A", a_level)
            sleep(step_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
