class ZulipRequestHandler:
    def __init__(self, zulipClient, username, screenSize):
        self.USERNAME = username
        self.zulipClient = zulipClient

    # Sends the zulip user who sent the message a response
    # either an "ok" or an error-message
    def send_response(self, response):
        self.zulipClient.send_message(response)

    def get_msg_to(self, msg):
        if msg["type"] == "stream":
            # user message was public
            msgTo = msg["display_recipient"]    # name of the stream

        elif msg["type"] == "private":
            # message sent by user is a private stream message
            msgTo = msg["sender_email"]

        return msgTo
