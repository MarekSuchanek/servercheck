import os
import subprocess

from .check import Check, CheckResult, MessageType


class SystemService(Check):

    origin = 'System service'

    states = {
        True: "running",
        False: "not running",
        None: "unknown"
    }

    state2mgstype = {
        True: MessageType.INFO,
        False: MessageType.WARNING,
        None: MessageType.ERROR
    }

    def __init__(self, service_name):
        self.service_name = service_name
        self.status = None
        super().__init__()

    @property
    def is_ok(self):
        return self.status is True

    def perform_check(self):
        try:
            self.status = is_service_running(self.service_name)
        except Exception:
            self.status = None

        if self.became_fixed:
            self.prev_ok = True
            return self.make_result(self.message[0], MessageType.GREAT_AGAIN)
        if self.became_broken:
            self.prev_ok = False
            return self.make_result(*self.message)
        return self.make_result(self.message[0], MessageType.INFO)

    @property
    def message(self):
        msg = "{} is {}".format(
            self.name, self.states[self.status]
        )
        msg_type = self.state2mgstype[self.status]
        return msg, msg_type

    @property
    def name(self):
        return "Service({})".format(self.service_name)


def is_service_running(name):
    with open(os.devnull, 'wb') as hide_output:
        exit_code = subprocess.Popen(['service', name, 'status'],
                                     stdout=hide_output,
                                     stderr=hide_output).wait()
        return exit_code == 0
