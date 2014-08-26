# Standard library
import re
from threading import Thread, Lock
import time
import requests

# Third party library
import zulip

# Local library
import imageRenderer as ImageRenderer
import messageQueue as MessageQueue
import opc
import textRenderer as TextRenderer
from zulipRequestHandler import ZulipRequestHandler

# LED Screen physical dimensions
MAX_FRAME_COUNT = 100
SCREEN_SIZE = (64, 32)
MATRIX_WIDTH, MATRIX_HEIGHT = SCREEN_SIZE
MATRIX_SIZE = MATRIX_WIDTH * MATRIX_HEIGHT

# Where to find the LED screen.
LED_SCREEN_ADDRESS = 'ledbone.local:7890'

# Zulip Conf. Zulip API_KEY is loaded from a file calleed API_KEY
# which is expected to be at the application root.
ZULIP_USERNAME = "led-bot@students.hackerschool.com"
api_file = open('API_KEY', 'r')
API_KEY = api_file.read()

###########################
# Components
###########################

# messageQueue is where incoming messages are stored and fetched from
messageQueue = MessageQueue.MessageQueue()

class LEDBot(object):

    def __init__(self, client):

        self.client = client

        # If string starts with "@led-bot" or "led-bot"
        self.USERNAME = ZULIP_USERNAME
        self.BOT_MSG_PREFIX = '^(\\@\\*\\*)*led-bot(\\*\\*)*'

        # Screen information
        self.SCREEN_SIZE = SCREEN_SIZE
        self.screen_width, self.screen_height = self.SCREEN_SIZE
        # opcClient is the Open Pixel Control client which provides the drivers
        # (using LEDscape) an API to the LED-screen
        self.opcClient = opc.Client(LED_SCREEN_ADDRESS)

        # Renderers
        self.text_renderer = TextRenderer.TextRenderer()
        self.image_renderer = ImageRenderer.ImageRenderer(self.SCREEN_SIZE)

        self._lock = Lock()

    def run(self):
        """ Run the main loop of the bot. """

        # running / blocking task
        # gets messages from messageQueue
        print('Trying to connect to LED-display...')
        if self.opcClient.can_connect():
            print('connected to %s' % LED_SCREEN_ADDRESS)

        print("Bot running... ")
        # Blocking call to zulip bot
        zulipClient.call_on_each_message(self.handle_message)

    def handle_message(self, msg):
        # This will have to do ALL actions for the main loop.
        # Queue incoming messages
        # Check queue for the next message
        # Process that message
        # Show it to the screen
        #   - manage the displayed frames / scrolling etc
        if self._is_bot_message(msg):
            token = self._get_msg_queue_token(msg)
            if token is not None:
                messageQueue.enqueue(token)
            self._send_response(token, msg)

        # TODO - ADD TIMER / FRAME COUNTER
        if not messageQueue.isEmpty():
            nextMsg = messageQueue.dequeue()

            # Display of message needs to happen in its own thread
            # to avoid blocking the message read process. If not done,
            # messages sent to bot during display activity would be ignored.
            thread = Thread(target=self.scroll_message, args=(nextMsg["image"],))
            thread.daemon = False
            thread.start()

    def scroll_message(self, image):
        """ Scroll the image through the screen. """

        frame_count = len(image)
        max_x_offset = image[0].size[0] + 1
        frame = 0
        counter = 0

        self._lock.acquire()

        for i in xrange(max_x_offset + MATRIX_WIDTH):
            time.sleep(1.0 / 60)
            self._show_image(image[frame], x_offset=i - MATRIX_WIDTH)
            counter = counter % 5
            if counter == 0:
                # for animated GIFs
                # if image has multiple frames change frame on every 5th scroll step
                frame = (frame + 1) % (frame_count)
            counter += 1

        self._lock.release()

    #### Private protocol #####################################################

    def _is_bot_message(self, msg):
        """ Return True if the message is meant for the bot. """

        return (
            msg["sender_email"] != self.USERNAME and

            re.match(self.BOT_MSG_PREFIX, msg["content"], flags=re.I or re.X)
        )

    def _get_msg_queue_token(self, msg):
        msgToken = self._tokenize_message(msg)

        if msgToken["type"] == "error":
            queue_token = None

        elif msgToken["type"] == "text":
            queue_token = self.text_renderer.get_queue_token(msgToken)

        elif msgToken["type"] == "image":
            queue_token = self.image_renderer.get_queue_token(msgToken)

        return queue_token

    def _send_response(self, queue_token, msg):
        # if queue item valid, send response to user
        if queue_token is None:
            user_response = self._get_response(msg, "syntaxError")

        elif queue_token["valid"]:
            user_response = self._get_response(msg)

        else:
            user_response = self._get_response(msg, "unknownError")

        self.client.send_response(user_response)

    def _tokenize_message(self, msg):
        """ Tokenizes a message. """

        tokens = re.sub(self.BOT_MSG_PREFIX, '', msg["content"]).split()

        if tokens[0] == "show-image":
            token = {
                "type" : "image",
                "url": tokens[1]
            }

        elif tokens[0] == "show-text":
            token = {
                "type" : "text",
                "text": tokens[1:]
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
            "type": msg["type"],
            "subject": msg["subject"],           # topic within the stream
            "to": self.client.get_msg_to(msg),         # name of the stream
            "content": "%s" % msgText        # message to print to stream
        }

        return response

    def _show_image(self, image, x_offset=0, y_offset=0):
        """Puts the image on the screen.

        Image is expected to be a Pillow object.

        NOTE: This method shouldn't be called without acquiring the lock for
        the screen.  When using this to add more functionality, make sure that
        the lock is acquired first.

        """

        # print("Image size", image.size)
        my_pixels = []
        image_width, image_height = image.size

        for i in xrange(0, MATRIX_SIZE):
            x = i % MATRIX_WIDTH + x_offset
            y = int(i / MATRIX_WIDTH) + y_offset
            #a = None
            if (x > 0) and (x < image_width) and (y > 0) and (y < image_height):
                r, g, b, a = image.getpixel((x, y))
                if a == 0:
                    r, g, b = 0, 0, 0
                my_pixels.append((b, g, r))
            else:
                my_pixels.append((0, 0, 0))

        # dump data to LED display
        self.opcClient.put_pixels(my_pixels, channel=0)


def get_zulip_streams():
    """ Get all the streams on Zulip, using the API.

    # Thanks Tristan!
    """

    response = requests.get(
        'https://api.zulip.com/v1/streams',
        auth=requests.auth.HTTPBasicAuth(ZULIP_USERNAME, API_KEY)
    )

    if response.status_code == 200:
        return response.json()['streams']

    elif response.status_code == 401:
        raise('check yo auth')

    else:
        raise(':( we failed to GET streams.\n(%s)' % response)

def subscribe_to_threads(zulipClient):
    """ Add subscriptions to the bot inorder to receive messages. """

    streams = [
        {'name': stream['name']} for stream in get_zulip_streams()
    ]
    zulipClient.add_subscriptions(streams)

if __name__ == '__main__':
    # Zulip python client by the good zulip-people.
    # Handles the polling (gets a callback) which is blocking
    # Also message sending etc
    zulipClient = zulip.Client(email=ZULIP_USERNAME, api_key=API_KEY)
    subscribe_to_threads(zulipClient)
    zulipRequestHandler = ZulipRequestHandler(
        zulipClient, ZULIP_USERNAME, SCREEN_SIZE
    )

    led_bot = LEDBot(client=zulipRequestHandler)
    led_bot.run()
