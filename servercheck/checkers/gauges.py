import psutil
from collections import deque

from .check import Check, CheckResult, MessageType


class Gauge(Check):

    origin = 'Gauge'
    name = 'Gauge'
    unit = '%'

    def __init__(self, threshold, average_of=1):
        self.threshold = threshold
        self.series = deque(maxlen=average_of)
        super().__init__()

    @property
    def size(self):
        return len(self.series)

    @property
    def average(self):
        return sum(self.series) / self.size

    @property
    def is_ok(self):
        return self.average < self.threshold

    def perform_check(self):
        self.series.append(self.measure())
        return CheckResult(self.is_ok, self.origin, *self.message)

    def measure(self):
        pass

    @property
    def message(self):
        msg = "{}: {}{}".format(self.name, self.series[-1], self.unit)
        msg_type = MessageType.INFO if self.is_ok else MessageType.WARNING
        return msg, msg_type


class CPUGauge(Gauge):

    origin = 'CPU'
    name = 'CPU'

    def measure(self):
        return psutil.cpu_percent()


class MemoryGauge(Gauge):

    origin = 'Memory'
    name = 'Memory'

    def measure(self):
        return psutil.virtual_memory().percent


class StorageGauge(Gauge):

    origin = 'Storage'

    def __init__(self, mount_point, threshold, average_of=1):
        self.mount_point = mount_point
        super().__init__(threshold, average_of)

    @property
    def name(self):
        return 'Storage({})'.format(self.mount_point)

    def measure(self):
        return psutil.disk_usage(self.mount_point).percent
