import click
import daemon
import logging
import yaml

from .daemon import ServerCheckDaemon
from .consts import PROGNAME, VERSION


LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'

@click.command()
@click.option('--cfg_file', '-c', type=click.File('r'),
              help='Path of the config YAML file.')
@click.option('--log_file', '-l', type=click.Path(),
              help='Logging file')
@click.option('--daemon', '-d', is_flag=True,
              help='Run in daemon mode')
@click.version_option(version=VERSION, prog_name=PROGNAME)
def servercheck(cfg_file, log_file, daemonize):
    cfg = yaml.load(cfg_file)
    sc_daemon = ServerCheckDaemon.create_from_config(cfg)

    if log_file is not None:
        logging.basicConfig(filename=log_file,
                            level=logging.DEBUG,
                            format=LOG_FORMAT)

    if daemonize:
        with daemon.DaemonContext():
            sc_daemon.run()
    else:
        sc_daemon.run()

