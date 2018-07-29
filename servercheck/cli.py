import click
import yaml


from .checking.gauges import CPUGauge, MemoryGauge, StorageGauge
from .checking.services import SystemService
from .checking.docker import DockerContainer


_gauge_type2cls = {
    'cpu': CPUGauge,
    'memory': MemoryGauge,
    'storage': StorageGauge
}


@click.command()
@click.option('--cfg_file', '-c', type=click.File('r'),
              help='Path of the config YAML file.')
def servercheck(cfg_file):
    cfg = yaml.load(cfg_file)
    checkers = []
    for gauge_type, settings in cfg['checks']['gauges'].items():
        gauge = _gauge_type2cls[gauge_type]
        checkers.append(gauge(**settings))
    for service in cfg['checks']['services']:
        checkers.append(SystemService(service))
    for container in cfg['checks']['docker']:
        checkers.append(DockerContainer(container))

    for c in checkers:
        print(c.perform_check())

