import logging
import math
from oscillator import Oscillator

from random import randint
from time import sleep

from estim_2b import Mode, commander
from ramp import Ramp, Sequence


logger = logging.getLogger(__name__)


def f(x):
    print("x", x)
    z = x * 4 * math.pi
    print("z", z)
    return z + math.sin(z - math.pi)


def g(x):
    return f(x) / f(1.0)


def h(x):
    y = g(x)
    y = max(y, 0.0)
    y = min(y, 1.0)
    return y


def main(
    start=30,
    rise=20,
    feel=90,
    active_seconds=0,
    inactive_seconds_min=5,
    inactive_seconds_max=20,
    num_shocks=50,
):
    seq = Sequence()

    with commander() as cmd:
        cmd.set_power("H")
        cmd.set_mode(Mode.CONTINUOUS)
        cmd.set_feel(feel)

        for i in range(num_shocks):
            x = i / num_shocks
            y = h(x)
            print("y", y)
            base_level = int(start + y * rise)

            cmd.set_level("A", base_level)
            sleep(active_seconds)
            cmd.set_level("A", 0)

            inactive_seconds = randint(inactive_seconds_min, inactive_seconds_max)
            sleep(inactive_seconds)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
