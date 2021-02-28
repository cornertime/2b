import logging

from random import randint
from time import sleep

from estim_2b import Mode, commander


logger = logging.getLogger(__name__)


def fate_dice(num_dice=4):
    return sum(randint(-1, 1) for i in range(num_dice))


def main(base_level=35, speed=70, feel=70, active_seconds=7, base_inactive_seconds=10):
    with commander() as cmd:
        cmd.set_mode(Mode.TRAINING)
        cmd.set_speed(speed)
        cmd.set_feel(feel)

        while True:
            # 35 + (-5..5) = 30..40
            level = base_level + fate_dice(5)
            cmd.set_level('A', level)

            logger.info('Sleeping in active cycle for %d seconds', active_seconds)
            sleep(active_seconds)
            cmd.set_level('A', 0)

            inactive_seconds = base_inactive_seconds + fate_dice(5)
            logger.info('Sleeping in inactive cycle for %d seconds', inactive_seconds)
            sleep(inactive_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()