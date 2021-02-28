import logging

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp


logger = logging.getLogger(__name__)


def fate_dice(num_dice=4):
    return sum(randint(-1, 1) for i in range(num_dice))


def main(ramp_start=45, ramp_end=65, ramp_seconds=20*60, speed=71, feel=80, active_seconds=10, base_inactive_seconds=10, safety_limit=70):
    ramp = Ramp(ramp_start, ramp_end, ramp_seconds)
    with commander() as cmd:
        cmd.set_mode(Mode.TRAINING)
        cmd.set_speed(speed)
        cmd.set_feel(feel)

        while True:
            # 35 + (-5..5) = 30..40
            level = ramp.get_value() + fate_dice(5)
            assert level <= safety_limit
            cmd.set_level('A', level)

            logger.info('Sleeping in active cycle for %d seconds', active_seconds)
            sleep(active_seconds)
            cmd.set_level('A', 0)

            inactive_seconds = base_inactive_seconds + fate_dice(5)
            logger.info('Sleeping in inactive cycle for %d seconds', inactive_seconds)
            sleep(inactive_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()