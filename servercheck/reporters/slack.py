import logging
import requests
import time

from ..checkers.check import MessageType
from .reporter import Reporter
from ..consts import FULLNAME


_msgtype2color = {
    MessageType.DEBUG: '#03109b',
    MessageType.INFO: '#119b04',
    MessageType.WARNING: '#c40000',
    MessageType.ERROR: '#c400a3',
    MessageType.FATAL: '#ffc700',
    MessageType.FIXED: '#097200',
}


class SlackWebhookCommunicator:

    def __init__(self, incoming_webhook, server_name, **opts):
        self.webhook = incoming_webhook
        self.server_name = server_name

    def _build_message(self, pretext, text, msg_type):
        return {
            'text': pretext,
            'attachments': [
                {
                    'title': '{}: {}'.format(self.server_name, msg_type.name),
                    'text': text,
                    'color': _msgtype2color[msg_type],
                    'footer': FULLNAME,
                    'ts': int(time.time())
                }
            ]
        }

    def send(self, pretext, text, msg_type):
        requests.post(
            self.webhook,
            json=self._build_message(pretext, text, msg_type)
        )
        # TODO: debug output on success/fail of sending


class SlackWebhookReporter(Reporter):

    def __init__(self, server_name, incoming_webhook):
        self.communicator = SlackWebhookCommunicator(incoming_webhook,
                                                     server_name)
        self.communicator.send(f'{server_name} - notice', 'ServerCheck started...', MessageType.DEBUG)

    def startup(self, server_name):
        pretext = f'Starting servercheck on "{server_name}"'
        msg = 'Any suspicious behaviour will be reported to this Slack channel.'
        self.communicator.send(pretext, msg, MessageType.INFO)

    def feed(self, messages):
        for msg in messages:
            if msg.message_type == MessageType.ERROR:
                pretext = f'{msg.origin} - error'
            elif msg.message_type == MessageType.WARNING:
                pretext = f'{msg.origin} - warning'
            elif msg.message_type == MessageType.FATAL:
                pretext = f'{msg.origin} - fatal error'
            elif msg.message_type == MessageType.FIXED:
                pretext = f'{msg.origin} - fixed'
            else:
                continue  # skipping others
            logging.getLogger().info(
                f'Sending to Slack({pretext},{msg.message},{msg.message_type.name})'
            )
            self.communicator.send(pretext, msg.message, msg.message_type)
