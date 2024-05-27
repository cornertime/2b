import logging

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp


logger = logging.getLogger(__name__)


def fate_dice(num_dice=4):
    return sum(randint(-1, 1) for i in range(num_dice))


START = 30
RISE = 40


def main(
    ramp_start=START,
    ramp_end=START + RISE,
    ramp_seconds=RISE * 60,
    speed=71,
    feel_min=20,
    feel_max=90,
    active_seconds=10,
    inactive_seconds_min=5,
    inactive_seconds_max=15,
):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)
    with commander() as cmd:
        cmd.set_power("H")
        cmd.set_mode(Mode.TRAINING)
        cmd.set_speed(speed)

        while True:
            # 35 + (-5..5) = 30..40
            feel = randint(feel_min, feel_max)
            cmd.set_feel(feel)

            level = ramp.get_value() + fate_dice(5)
            cmd.set_level("A", level)

            logger.info("Sleeping in active cycle for %d seconds", active_seconds)
            sleep(active_seconds)
            cmd.set_level("A", 0)

            inactive_seconds = randint(inactive_seconds_min, inactive_seconds_max)
            logger.info("Sleeping in inactive cycle for %d seconds", inactive_seconds)
            sleep(inactive_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
