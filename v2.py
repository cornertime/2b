import logging
from oscillator import Oscillator

from random import choice, randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp, Sequence


logger = logging.getLogger(__name__)

START = 25
RISE = 40
SEQUENCES = [
    [0, 2, 8],
    [0, 2, 4, 6],
    [0, 2, 4, 6, 7],
    [0, 2, 4, 6, 7, 8],
    [0, 2, 4, 6, 7, 8, 8, 8],
    [0, 2, 4, 6, 7, 8, 0, 8],
    [0, 2, 4, 6, 7, 8, 10],
]


def main(
    ramp_start=START,
    ramp_end=START + RISE,
    ramp_seconds=RISE * 90,
    warn_adjustment=3,
    feel=90,
    warn_seconds=1,
    active_seconds=0,
    inactive_seconds_min=5,
    inactive_seconds_max=20,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)
    time_osc = Oscillator(inactive_seconds_min, inactive_seconds_max, 120)

    with commander() as cmd:
        cmd.set_power("H")
        cmd.set_mode(Mode.CONTINUOUS)
        cmd.set_feel(feel)

        sequence = SEQUENCES[-1]

        while True:
            for seq_value in sequence:
                base_level = ramp.get_value() + seq_value
                warn_level = base_level // warn_adjustment

                cmd.set_level("A", warn_level)
                sleep(warn_seconds)
                cmd.set_level("A", base_level)
                sleep(active_seconds)
                cmd.set_level("A", 0)

                # inactive_seconds = randint(inactive_seconds_min, inactive_seconds_max)
                inactive_seconds = time_osc.get_value()
                sleep(inactive_seconds)

            sequence = choice(SEQUENCES)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
