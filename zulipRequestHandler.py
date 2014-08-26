# Standard library
import re

# 3rd party library
import requests
import zulip

class ZulipRequestHandler:

    def __init__(self, email, api_key):
        self.email = email

        # If string starts with "@led-bot" or "led-bot"
        self.bot_msg_prefix = '^(\\@\\*\\*)*led-bot(\\*\\*)*'

        self.api_key = api_key
        self.zulipClient = zulip.Client(email=email, api_key=api_key)
        self._subscribe_to_threads()

    def send_response(self, response, msg):
        """ Send the response to a user who sent a message to us. """

        response.update({
            "type": msg["type"],
            "subject": msg["subject"],   # topic within the stream
            "to": self.get_msg_to(msg),  # name of the stream
        })

        self.zulipClient.send_message(response)

    def get_msg_to(self, msg):
        if msg["type"] == "stream":
            # user message was public
            msgTo = msg["display_recipient"]    # name of the stream

        elif msg["type"] == "private":
            # message sent by user is a private stream message
            msgTo = msg["sender_email"]

        return msgTo

    def listen(self, callback):

        def handle_message(msg):
            if self._is_bot_message(msg):
                callback(msg, self)

        self.zulipClient.call_on_each_message(handle_message)

    def _is_bot_message(self, msg):
        """ Return True if the message is meant for the bot. """

        return (
            msg["sender_email"] != self.email and

            re.match(self.bot_msg_prefix, msg["content"], flags=re.I or re.X)
        )

    def _subscribe_to_threads(self):
        """ Add subscriptions to the bot inorder to receive messages. """

        streams = [
            {'name': stream['name']}

            for stream in get_zulip_streams(self.email, self.api_key)
        ]

        self.zulipClient.add_subscriptions(streams)


def get_zulip_streams(email, api_key):
    """ Get all the streams on Zulip, using the API.

    # Thanks Tristan!
    """

    response = requests.get(
        'https://api.zulip.com/v1/streams',
        auth=requests.auth.HTTPBasicAuth(email, api_key)
    )

    if response.status_code == 200:
        return response.json()['streams']

    elif response.status_code == 401:
        raise('check yo auth')

    else:
        raise(':( we failed to GET streams.\n(%s)' % response)
