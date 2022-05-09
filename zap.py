import logging
from oscillator import Oscillator

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp


logger = logging.getLogger(__name__)


def main(
    level=25,
    feel=80,
    active_seconds=2,
):
    with commander() as cmd:
        cmd.set_mode(Mode.CONTINUOUS)
        cmd.set_feel(feel)

        while True:
            cmd.set_level('A', level)
            sleep(active_seconds)
            cmd.set_level('A', 0)

            line = input()
            new_level = 0
            try:
                new_level = int(line)
            except ValueError:
                pass

            if 1 <= new_level <= 100:
                level = new_level



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()