from enum import Enum


class Check:

    origin = 'Generic'

    def __init__(self):
        self.prev_ok = True

    @property
    def is_ok(self):
        return True

    @property
    def became_broken(self):
        return self.prev_ok and not self.is_ok

    @property
    def became_fixed(self):
        return self.is_ok and not self.prev_ok

    @property
    def still_same(self):
        return self.is_ok == self.prev_ok

    def update_prev(self):
        self.prev_ok = self.is_ok

    def perform_check(self):
        return self.make_result('Ping', MessageType.DEBUG)

    def make_result(self, message, message_type):
        return CheckResult(self.is_ok, self.origin, message, message_type)


class CheckResult:

    def __init__(self, ok, origin, message, message_type):
        self.ok = ok
        self.origin = origin
        self.message = message
        self.message_type = message_type

    def __str__(self):
        return self.message


class MessageType(Enum):
    DEBUG=0
    INFO=1
    WARNING=2
    ERROR=3
    FATAL=4
    FIXED=5
