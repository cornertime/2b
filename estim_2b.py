import logging
import platform
from collections import namedtuple
from contextlib import contextmanager
from enum import Enum, IntEnum
from typing import Optional

from serial import Serial

logger = logging.getLogger(__name__)
FAKE_REPLY_BYTES = b"100:40:0:50:50:13:L:0:1.04\r"
BAUD_RATE = 9600
SERIAL_PORT = "COM3" if platform.system() == "Windows" else "/dev/cu.usbserial-FTGZ75LA"


class Mode(IntEnum):
    PULSE = 0
    BOUNCE = 1
    CONTINUOUS = 2
    A_SPLIT = 3
    B_SPLIT = 4
    WAVE = 5
    WATERFALL = 6
    SQUEEZE = 7
    MILK = 8
    THROB = 9
    THRUST = 10
    RANDOM = 11
    STEP = 12
    TRAINING = 13
    MICROPHONE = 14
    STEREO = 15


FEEL_PARAM_BY_MODE = {
    Mode.PULSE: "D",
    Mode.BOUNCE: "D",
    Mode.CONTINUOUS: "C",
    Mode.A_SPLIT: "D",
    Mode.B_SPLIT: "D",
    Mode.WAVE: "D",
    Mode.WATERFALL: "D",
    Mode.SQUEEZE: "D",
    Mode.MILK: "D",
    Mode.THROB: "C",
    Mode.THRUST: "C",
    Mode.RANDOM: "D",
    Mode.STEP: "D",
    Mode.TRAINING: "D",
    Mode.MICROPHONE: "C",
    Mode.STEREO: "C",
}

SPEED_PARAM_BY_MODE = {
    Mode.PULSE: "C",
    Mode.BOUNCE: "C",
    Mode.A_SPLIT: "C",
    Mode.B_SPLIT: "C",
    Mode.WAVE: "C",
    Mode.WATERFALL: "C",
    Mode.SQUEEZE: "C",
    Mode.MILK: "C",
    Mode.RANDOM: "C",
}

DELAY_PARAM_BY_MODE = {
    Mode.STEP: "C",
    Mode.TRAINING: "C",
}


class Command(Enum):
    A_LEVEL = "A"
    B_LEVEL = "B"
    C_SETTING = "C"
    D_SETTING = "D"
    RESET = "E"
    HIGH_POWER = "H"
    JOIN_CHANNELS = "J"
    ZERO = "K"
    LOW_POWER = "L"
    MODE = "M"
    UNLINK_CHANNELS = "U"


EXPECTED_DEFAULTS = [0, 0, 50, 50, Mode.PULSE]


class Reply(
    namedtuple(
        "Reply",
        [
            "battery_level",
            "a_level",
            "b_level",
            "c_setting",
            "d_setting",
            "mode",
            "power_setting",
            "channels_joined",
            "firmware_version",
        ],
    )
):
    @classmethod
    def from_bytes(cls, data: bytes):
        """
        >>> Reply.from_bytes(FAKE_REPLY_BYTES)
        Reply(battery_level=100, a_level=40, b_level=0, c_setting=50, d_setting=50, mode=<Mode.TRAINING: 13>, power_setting='L', channels_joined=False, firmware_version='1.04')
        """
        (
            battery_level,
            a_level,
            b_level,
            c_setting,
            d_setting,
            mode,
            power_setting,
            channels_joined,
            firmware_version,
        ) = data.decode("ASCII").strip().split(":")

        return cls(
            int(battery_level),
            int(a_level),
            int(b_level),
            int(c_setting),
            int(d_setting),
            Mode(int(mode)),
            power_setting,
            bool(int(channels_joined)),
            firmware_version,
        )


class Commander:
    serial: Optional[Serial]

    def __init__(self, serial: Optional[Serial] = None):
        """
        Do not call directly, instead use the `commander` context manager.
        """
        self.serial = serial
        self.mode = Mode.PULSE

    def _send(self, command: Command, param: Optional[int] = None):
        """
        Do not call directly, instead use the `reset`, `set_mode`, `set_feel`, `set_level`
        and `set_speed` methods.
        """
        logger.info("Sending %s %s", command, "" if param is None else param)
        param_str = "" if param is None else str(param)
        cmd_bytes = f"{command.value}{param_str}\r".encode()
        logger.debug("-> %r", cmd_bytes)

        if self.serial:
            # Actual serial port mode
            self.serial.write(cmd_bytes)
            reply_bytes = self.serial.read_until(b"\r")
        else:
            # Dry run mode
            reply_bytes = FAKE_REPLY_BYTES

        logger.debug("<- %r", reply_bytes)
        reply = Reply.from_bytes(reply_bytes)
        logger.info("Got %s", reply)

        return reply

    def set_mode(self, mode: Mode):
        reply = self._send(Command.MODE, mode.value)
        if reply.mode != mode:
            raise TypeError(f"Requested mode {mode.value}, device reported {reply}")
        self.mode = mode

    def reset(self):
        """
        Sets A = 0, B = 0, C = 50, D = 50, mode = PULSE.
        """
        _reply = self._send(Command.RESET)
        # if [reply.a_level, reply.b_level, reply.c_setting, reply.d_setting, reply.mode] != EXPECTED_DEFAULTS:
        #     raise TypeError(f'State not as expected after reset: {reply}')

    def set_feel(self, feel: int):
        """
        Sets the "feel" parameter. Higher is generally spikier, lower is smoother.
        Note that not all modes have a feel parameter. An exception is raised if
        `set_feel` is called in a mode that doesn't.
        """
        assert 2 <= feel <= 99
        feel_param = FEEL_PARAM_BY_MODE.get(self.mode)
        if not feel_param:
            raise TypeError(f"Mode {self.mode} does not have a feel parameter")
        self._send(Command(feel_param), feel)

    def _set_delay(self, delay: int):
        assert 2 <= delay <= 99
        delay_param = DELAY_PARAM_BY_MODE[self.mode]
        self._send(Command(delay_param), delay)

    def set_speed(self, speed: int):
        """
        Sets the "speed" parameter.  For modes that have a "delay" parameter instead,
        speed is correctly reversed. Higher is always faster, lower is always slower.
        Note that not all modes have a speed parameter. An exception is raised if
        `set_speed` is called in a mode that doesn't.
        """
        assert 2 <= speed <= 99

        if self.mode in DELAY_PARAM_BY_MODE:
            # This mode has delay instead of speed, so flip it
            # Delay 2 is fastest, corresponds to speed 99
            # Delay 99 is slowest, corresponds to speed 2
            return self._set_delay(100 - speed + 1)

        speed_param = SPEED_PARAM_BY_MODE.get(self.mode)
        if not speed_param:
            raise TypeError(f"Mode {self.mode} does not have a speed/delay parameter")

        self._send(Command(speed_param), speed)

    def set_level(self, channel, level):
        assert channel in ["A", "B"]
        assert 0 <= level <= 100
        return self._send(Command(channel), level)

    def set_power(self, power):
        assert power in ["L", "H"]
        return self._send(Command(power))


@contextmanager
def commander(serial_port=SERIAL_PORT, timeout_seconds=1.0):
    """
    The preferred way to get a Commander instance. Handles serial port
    opening/closing and performs a reset (E command) at both the start and end
    of the session.
    """
    commander = None
    with Serial(serial_port, BAUD_RATE, timeout=timeout_seconds) as serial:
        try:
            # commander = Commander()
            commander = Commander(serial)
            commander.reset()
            yield commander
        except (Exception, KeyboardInterrupt):
            if commander:
                # just reset without checks
                commander._send(Command.RESET)
            raise
