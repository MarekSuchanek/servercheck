from enum import Enum


class Check:

    @property
    def is_ok(self):
        return True

    def perform_check(self):
        return CheckResult(True, "Generic", "OK", MessageType.DEBUG)


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
    GREAT_AGAIN=5
