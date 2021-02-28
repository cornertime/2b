import logging
from time import monotonic


logger = logging.getLogger(__name__)


class Ramp:
    min_value: int
    max_value: int
    period_seconds: int

    def __init__(self, min_value=30, max_value=50, period_seconds=20 * 60):
        self.min_value = min_value
        self.max_value = max_value
        self.period_seconds = period_seconds
        self.start_time = monotonic()

    def get_value(self):
        seconds_passed = monotonic() - self.start_time
        frac_passed = seconds_passed / self.period_seconds
        value = int(min(frac_passed * (self.max_value - self.min_value) + self.min_value, self.max_value))
        logger.info('Ramp: Time %d / %d seconds, value %d / %d', seconds_passed, self.period_seconds, value, self.max_value)
        return value