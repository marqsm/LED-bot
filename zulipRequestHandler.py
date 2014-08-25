import re
import imageRenderer as ImageRenderer
import textRenderer as TextRenderer


class ZulipRequestHandler:
    def __init__(self, zulipClient, username, screenSize):
        self.SCREEN_SIZE = screenSize
        self.USERNAME = username
        # If string starts with "@led-bot" or "led-bot"
        self.BOT_MSG_PREFIX = '^(\\@\\*\\*)*led-bot(\\*\\*)*'
        self.zulipClient = zulipClient
        self.screen_width, self.screen_height = self.SCREEN_SIZE
        self.text_renderer = TextRenderer.TextRenderer()
        self.image_renderer = ImageRenderer.ImageRenderer(self.SCREEN_SIZE)
        return None

    # Main function, this is what gets passed to the actual Zulip Client
    def get_msg_queue_token(self, msg):
        self.msg = msg

        # Do stuff
        if self.isBotMessage(msg):
            print("is Bot message")
            msgToken = self.tokenizeMessage(msg)
            if msgToken["type"] == "error":
                user_response = self.getResponse(msg, "syntaxError")
                self.send_response(user_response)
                return None
                # Do we need to do something here?
            elif msgToken["type"] == "text":
                print "getMsgQueueToken text"
                queue_token = self.text_renderer.get_queue_token(msgToken)
            elif msgToken["type"] == "image":
                print "getMsgQueueToken image"
                queue_token = self.image_renderer.get_queue_token(msgToken)
                print("This is what I got from ImageRenderer")
                print(queue_token)

            # if queue item valid, send response to user
            if queue_token["valid"]:
                user_response = self.getResponse(msg)
                self.send_response(user_response)

                return queue_token
            else:
                user_response = self.getResponse(msg, "unknownError")
                self.send_response(user_response)
                return None

        return None

    # Sends the zulip user who sent the message a response
    # either an "ok" or an error-message
    def send_response(self, response):
        self.zulipClient.send_message(response)
        return None

    def tokenizeMessage(self, msg):
        arr = re.sub(self.BOT_MSG_PREFIX, '', msg["content"]).split()
        token = {}
        if arr[0] == "show-image":
            token["type"] = "image"
            token["url"] = arr[1]
        elif arr[0] == "show-text":
            token["type"] = "text"
            token["text"] = arr[1:]
        else:
            token["type"] = "error"

        print('tokenizeMessage: ', token)

        return token

    def get_msg_to(self, msg):
        if msg["type"] == "stream":
            # user message was public
            msgTo = msg["display_recipient"]    # name of the stream
        elif msg["type"] == "private":
            # message sent by user is a private stream message
            msgTo = msg["sender_email"]

        return msgTo

    # getResponse :: create response to message sender
    #   - ok-message
    #   - error-message
    #       - invalid syntax - explain how to use
    #       - Image load failed
    #       - WTF (aka "Something broke, I don't know what")
    def getResponse(self, msg, status="ok"):
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

        resp = {
            "type": msg["type"],
            "subject": msg["subject"],           # topic within the stream
            "to": self.get_msg_to(msg),         # name of the stream
            "content": "%s" % msgText        # message to print to stream
        }

        return resp

    # Checks if message is meant for the bot
    def isBotMessage(self, msg):
        if (msg["sender_email"] != self.USERNAME
                and (re.match(self.BOT_MSG_PREFIX, msg["content"],
                              flags=re.I or re.X))):
            return True
        return False
