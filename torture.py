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
    ramp_seconds=RISE * 120,
    feel=90,
    speed=5,
    seq_min=-10,
    seq_max=10,
    seq_step=1,
    step_seconds=5,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)
    seq = Sequence(min_value=seq_min, max_value=seq_max, step=seq_step)

    with commander() as cmd:
        cmd.set_power("H")
        cmd.set_mode(Mode.RANDOM)
        cmd.set_speed(speed)
        cmd.set_feel(feel)

        while True:
            level = ramp.get_value()
            level += max(seq.get_value(), 0)

            cmd.set_level("A", level)
            sleep(step_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
