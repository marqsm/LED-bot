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
        #response.update({
        #    "type": msg["type"],
        #    "subject": "test",   # topic within the stream
        #    "to": self.get_msg_to(msg),  # name of the stream
        #})

        #self.zulipClient.send_message(response)

    def get_msg_to(self, msg):
        # message sent by user is a private stream message
        msgTo = msg["sender_email"]

        return msgTo

    def listen(self, callback):

        def handle_message(msg):
            if self._is_bot_message(msg):
                tokenized_msg = self._tokenize_message(msg)
                callback(tokenized_msg, self)

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

    def _tokenize_message(self, msg):
        """ Tokenizes a message. """

        tokens = re.sub(self.bot_msg_prefix, '', msg["content"]).split()

        # get index of emoji and its URL

        if tokens[0] == "show-image":
            token = {
                "type" : "image",
                "url": tokens[1],
            }

        elif tokens[0] == "show-text":
            token = {
                "type" : "text",
                "text": tokens[1:],
                "color":(0,120,0)           
            }

        else:
            token = {
                "type" : "error",
            }

        return token

        def _get_response(self, msg, status="ok"):
            """ Return a response to send to the user.

            #   - ok-message
            #   - error-message
            #       - invalid syntax - explain how to use
            #       - Image load failed
            #       - WTF (aka "Something broke, I don't know what")

            """

            if status == "ok":
                msgText = """JUST GIVE ME A SEC I'LL SHOW YOUR STUFF WHEN I CAN!
                             WE'RE ALL UNDER A LOT OF PRESSURE HERE!!!"""

            elif status == "syntaxError":
                msgText = """I don't know what that is.. you could try sending me
                              led-bot show-image http://www.example.com/cat.gif
                              led-bot show-text whatever you want to say"""

            elif status == "imageLoadError":
                msgText = """WHAT KIND OF IMAGES ARE YOU TRYING TO SEND ME
                             I DONT KNOW WHAT THAT STUFF IS!! """

            elif status == "unknownError":
                msgText = """ WTF WAS THAT SOMETHING BROKE
                              AND I HAVE NO IDEA WHAT IT WAS!"""
            else:
                msgText = "Yeah, this default message should never be reached.."

            response = {
                "content": "%s" % msgText,  # message to print to stream
            }

            return response

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
        raise RuntimeError('check yo auth')

    else:
        raise RuntimeError(':( we failed to GET streams.\n(%s)' % response)
