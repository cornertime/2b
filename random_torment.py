import logging

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp
from oscillator import Oscillator


logger = logging.getLogger(__name__)


def fate_dice(num_dice=4):
    return sum(randint(-1, 1) for i in range(num_dice))


START = 40
RISE = 40


def main(
    ramp_start=START,
    ramp_end=START + RISE,
    ramp_seconds=RISE * 90,
    warn_level=13,
    feel=90,
    warn_seconds=1,
    dice_modifier=2,
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

        while True:
            base_level = ramp.get_value()
            level = base_level + dice_modifier * abs(fate_dice())

            cmd.set_level("A", warn_level)
            sleep(warn_seconds)
            cmd.set_level("A", level)
            sleep(active_seconds)
            cmd.set_level("A", 0)

            # inactive_seconds = randint(inactive_seconds_min, inactive_seconds_max)
            inactive_seconds = time_osc.get_value()
            sleep(inactive_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
