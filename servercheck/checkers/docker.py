import docker

from enum import Enum

from .check import Check, MessageType


def container_states():
    docker_client = docker.from_env()
    return {c.name: c.status for c in docker_client.containers.list()}


class DockerContainer(Check):

    origin = 'Docker'

    def __init__(self, container_name):
        self.container_name = container_name
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

        if self.became_fixed:
            self.prev_ok = True
            return self.make_result(self.message[0], MessageType.FIXED)
        if self.became_broken:
            self.prev_ok = False
            return self.make_result(*self.message)
        return self.make_result(self.message[0], MessageType.INFO)

    @property
    def message(self):
        if DockerContainerStatus.ERROR:
            msg = f'{self.name} - error occured while communicating with Docker'
        elif DockerContainerStatus.UNKNOWN:
            msg = f'{self.name} cannot be determined'
        else:
            msg = f'{self.name} is in state "{self.status.name}"'

        msg_type = _status2msgtype.get(self.status, MessageType.WARNING)
        return msg, msg_type

    @property
    def name(self):
        return f'Docker({self.container_name})'


class DockerContainerStatus(Enum):
    CREATED = 0
    RESTARTING = 1
    RUNNING = 2
    REMOVING = 3
    PAUSED = 4
    EXITED = 5
    DEAD = 6
    UNKNOWN = 7
    ERROR = 8


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
