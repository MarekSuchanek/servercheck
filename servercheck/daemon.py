import time

from .checkers.gauges import CPUGauge, MemoryGauge, StorageGauge
from .checkers.services import SystemService
from .checkers.docker import DockerContainer
from .reporters.slack import SlackWebhookReporter


_gauge_type2cls = {
    'cpu': CPUGauge,
    'memory': MemoryGauge,
    'storage': StorageGauge
}


_reporter_type2cls = {
    'slack': SlackWebhookReporter
}


class ServerCheckDaemon:

    def __init__(self, server_name, check_period):
        self.server_name = server_name
        self.check_period = check_period
        self.checkers = []
        self.reporters = []

    def run(self):
        while True:
            msgs = [c.perform_check() for c in self.checkers]
            for reporter in self.reporters:
                reporter.feed(msgs)
            time.sleep(self.check_period)

    @staticmethod
    def create_from_config(cfg):
        d = ServerCheckDaemon(
            cfg['server_name'],
            int(cfg['check_period'])
        )
        for gauge_type, settings in cfg['checkers'].get('gauges', {}).items():
            gauge = _gauge_type2cls[gauge_type]
            d.checkers.append(gauge(**settings))
        for service in cfg['checkers'].get('services', []):
            d.checkers.append(SystemService(service))
        for container in cfg['checkers'].get('docker', []):
            d.checkers.append(DockerContainer(container))

        for reporter_type, settings in cfg.get('reporters', {}).items():
            settings['server_name'] = cfg['server_name']
            reporter = _reporter_type2cls[reporter_type]
            d.reporters.append(reporter(**settings))

        return d
