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
    MessageType.FATAL: '#ffc700'
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
        self.communicator = SlackWebhookCommunicator(server_name,
                                                     incoming_webhook)

    def feed(self, messages):
        for msg in messages:
            if msg.message_type == MessageType.ERROR:
                pretext = '{} - error'
            elif msg.message_type == MessageType.WARNING:
                pretext = '{} - warning'
            elif msg.message_type == MessageType.FATAL:
                pretext = '{} - fatal error'
            else:
                continue
            pretext = pretext.format(msg.origin)
            logging.getLogger().info(
                'Sending to Slack({},{},{})'.format(pretext, msg.message, msg.message_type.name)
            )
            self.communicator.send(pretext, msg.message, msg.message_type)
