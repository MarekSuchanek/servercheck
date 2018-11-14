import docker

from enum import Enum

from .check import Check, CheckResult, MessageType


docker_client = docker.from_env()


def container_states():
    return {c.name: c.status for c in docker_client.containers.list()}


class DockerContainer(Check):

    origin = 'Docker'

    def __init__(self, container_name):
        self.container_name = container_name
        self.prev_status = DockerContainerStatus.UNKNOWN
        self.status = DockerContainerStatus.UNKNOWN
        super().__init__()

    @property
    def is_ok(self):
        return self.status == DockerContainerStatus.RUNNING

    def perform_check(self):
        try:
            states = container_states()
            state = states.get(self.container_name, 'unknown')
            self.status = _string2status.get(state, DockerContainerStatus.UNKNOWN)
        except Exception:
            self.status = DockerContainerStatus.ERROR
        prev = self.prev_status
        self.prev_status = self.status
        if not prev == self.status and self.is_ok:  # fixed
            return CheckResult(self.is_ok, self.origin,
                               self.message[0], MessageType.GREAT_AGAIN)
        if prev == self.status:  # still failing or still ok
            return CheckResult(self.is_ok, self.origin,
                               self.message[0], MessageType.INFO)
        return CheckResult(self.is_ok, self.origin, *self.message)

    @property
    def message(self):
        if DockerContainerStatus.ERROR:
            msg = "{} - error occured while communicating with Docker".format(
                self.name
            )
        elif DockerContainerStatus.UNKNOWN:
            msg = "{} cannot be determined".format(
                self.name
            )
        else:
            msg = "{} is in state \"{}\"".format(
                self.name, self.status.name
            )

        msg_type = _status2msgtype.get(self.status, MessageType.WARNING)
        return msg, msg_type

    @property
    def name(self):
        return "Docker({})".format(self.container_name)


class DockerContainerStatus(Enum):
    CREATED=0
    RESTARTING=1
    RUNNING=2
    REMOVING=3
    PAUSED=4
    EXITED=5
    DEAD=6
    UNKNOWN=7
    ERROR=8


_string2status = {
    'created': DockerContainerStatus.CREATED,
    'restarting': DockerContainerStatus.RESTARTING,
    'running': DockerContainerStatus.RUNNING,
    'removing': DockerContainerStatus.REMOVING,
    'paused': DockerContainerStatus.PAUSED,
    'exited': DockerContainerStatus.EXITED,
    'dead': DockerContainerStatus.DEAD
}


_status2msgtype = {
    DockerContainerStatus.ERROR: MessageType.ERROR,
    DockerContainerStatus.RUNNING: MessageType.INFO
}
