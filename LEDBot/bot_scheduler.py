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

###########################
# Components
###########################

# message_queue is where incoming messages are stored and fetched from
message_queue = Queue()


class LEDBot(object):

    def __init__(self, address, listeners=None):

        self.address = address
        self.listeners = listeners if listeners is not None else []

        # If string starts with "@led-bot" or "led-bot"
        # fixme: duplicated
        #self.BOT_MSG_PREFIX = '^(\\@\\*\\*)*led-bot(\\*\\*)*'

        # Screen information
        self.SCREEN_SIZE = SCREEN_SIZE
        self.screen_width, self.screen_height = self.SCREEN_SIZE
        # opcClient is the Open Pixel Control client which provides the drivers
        # (using LEDscape) an API to the LED-screen
        self.opcClient = opc.Client(address)

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
            print('connected to %s' % self.address)

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
        #msgToken = self._tokenize_message(msg)

        if msg["type"] == "error":
            queue_token = None

        elif msg["type"] == "text":
            queue_token = self.text_renderer.get_queue_token(msg)

        elif msg["type"] == "image":
            queue_token = self.image_renderer.get_queue_token(msg)

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

        # We reverse the string, to adjust for some wonkiness with PIL output
        # being RGB but OPC library "expecting" BRG.  (It may be something
        # wonky in our hardware setup/config, too)
        data = cropped_image.tobytes()[::-1]

        # dump data to LED display
        self.opcClient.put_data(data, channel=0)

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

def main():
    """ Main entry point.

    Used in the console script we setup.

    """

    from zulipRequestHandler import ZulipRequestHandler
    from webFillerHandler import WebFillerHandler
    from webRequestHandler import WebRequestHandler

    from utils import get_config

    config = get_config()
    ZULIP_USERNAME = config.get('zulip', 'username')
    ZULIP_API_KEY = config.get('zulip', 'api_key')
    HTTP_SERVER_HOST = config.get('http', 'host')
    HTTP_SERVER_PORT = config.get('http', 'port')
    LED_SCREEN_ADDRESS = config.get('main', 'led_screen_address')
    FILLER_TIME_INTERVAL = config.get('fillers','time_interval')

    zulipRequestHandler = ZulipRequestHandler(ZULIP_USERNAME, ZULIP_API_KEY)
    webRequestHandler = WebRequestHandler(HTTP_SERVER_HOST,HTTP_SERVER_PORT)
    webFillerHandler = WebFillerHandler(FILLER_TIME_INTERVAL)
    
    led_bot = LEDBot(
        address=LED_SCREEN_ADDRESS, listeners=[zulipRequestHandler,webRequestHandler,webFillerHandler]
    )

    ## Uncomment the lines below to be able to test the bot from the CLI.
    # from cli_handler import CLIHandler
    # led_bot = LEDBot(
    #     address=LED_SCREEN_ADDRESS,
    #     listeners=[CLIHandler(), zulipRequestHandler]
    # )

    led_bot.run()


if __name__ == '__main__':
    main()
