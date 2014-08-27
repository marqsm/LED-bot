# Standard library
import re
from Queue import Queue
from threading import Thread, Lock
import time
import logging

# Local library
import imageRenderer as ImageRenderer
import opc
import textRenderer as TextRenderer

# LED Screen physical dimensions
MAX_FRAME_COUNT = 100
SCREEN_SIZE = (64, 32)
MATRIX_WIDTH, MATRIX_HEIGHT = SCREEN_SIZE
MATRIX_SIZE = MATRIX_WIDTH * MATRIX_HEIGHT

# Where to find the LED screen.
LED_SCREEN_ADDRESS = 'ledbone.local:7890'

# Zulip Conf.
ZULIP_USERNAME = "led-bot@students.hackerschool.com"
# Zulip API_KEY is loaded from a file called API_KEY at the app root.
with open('API_KEY', 'r') as api_file:
    API_KEY = api_file.read().strip()

###########################
# Components
###########################

# message_queue is where incoming messages are stored and fetched from
message_queue = Queue()

class LEDBot(object):

    def __init__(self, listeners=None):

        self.listeners = listeners if listeners is not None else []

        # If string starts with "@led-bot" or "led-bot"
        # fixme: duplicated
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
        # gets messages from message_queue
        print('Trying to connect to LED-display...')
        if self.opcClient.can_connect():
            print('connected to %s' % LED_SCREEN_ADDRESS)

        # Start up each of the listeners in a different thread
        self._start_listeners()

        print("Bot running... ")

        # Set up logging.
        logging.basicConfig(filename='led-bot.log',level=logging.INFO)

        # The main event loop, process any messages in the queue
        while True:
            time.sleep(0.1)
            self._process_queue()

    def handle_message(self, msg, listener):
        token = self._process_message(msg)
        if token is not None:
            # Add msg to log.
            logging.info(msg)
            message_queue.put(token)
        self._send_response(token, msg, listener)

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

    def _process_message(self, msg):
        msgToken = self._tokenize_message(msg)

        if msgToken["type"] == "error":
            queue_token = None

        elif msgToken["type"] == "text":
            queue_token = self.text_renderer.get_queue_token(msgToken)

        elif msgToken["type"] == "image":
            queue_token = self.image_renderer.get_queue_token(msgToken)

        return queue_token

    def _send_response(self, queue_token, msg, listener):
        # if queue item valid, send response to user
        if queue_token is None:
            user_response = self._get_response(msg, "syntaxError")

        elif queue_token["valid"]:
            user_response = self._get_response(msg)

        else:
            user_response = self._get_response(msg, "unknownError")

        listener.send_response(user_response, msg)

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
            "content": "%s" % msgText,  # message to print to stream
        }

        return response

    def _show_image(self, image, x_offset=0, y_offset=0):
        """Puts the image on the screen.

        Image is expected to be a Pillow object.

        NOTE: This method shouldn't be called without acquiring the lock for
        the screen.  When using this to add more functionality, make sure that
        the lock is acquired first.

        """

        image_width, image_height = image.size

        cropped_image = image.crop((
            0+x_offset,  # left
            0+y_offset,  # upper
            MATRIX_WIDTH + x_offset,  # right
            MATRIX_HEIGHT + y_offset  # lower
        ))

        pixels = cropped_image.getdata()

        # dump data to LED display
        self.opcClient.put_pixels(pixels, channel=0)

    def _start_listeners(self):
        for listener in self.listeners:
            thread = Thread(target=listener.listen, args=(self.handle_message,))
            thread.daemon = True
            thread.start()

    def _process_queue(self):
        """Process messages in the queue.

        Checks the queue and processes the first message on the queue.

        """

        if not message_queue.empty():
            nextMsg = message_queue.get(block=False)

            # Display of message needs to happen in its own thread
            # to avoid blocking the message read process. If not done,
            # messages sent to bot during display activity would be ignored.
            thread = Thread(target=self.scroll_message, args=(nextMsg["image"],))
            thread.daemon = False
            thread.start()


if __name__ == '__main__':
    from zulipRequestHandler import ZulipRequestHandler
    zulipRequestHandler = ZulipRequestHandler(ZULIP_USERNAME, API_KEY)
    led_bot = LEDBot(listeners=[zulipRequestHandler])

    # Uncomment the lines below to be able to test the bot from the CLI.
    # from cli_handler import CLIHandler
    # led_bot = LEDBot(listeners=[CLIHandler(), zulipRequestHandler])

    led_bot.run()
