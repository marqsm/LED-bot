import messageQueue as MessageQueue
import zulipRequestHandler as ZulipRequestHandler
import zulip
import opc
from threading import Thread, Lock
import time
import requests
import json


# LED Screen physical dimensions
MAX_FRAME_COUNT = 100
SCREEN_SIZE = (64, 32)
MATRIX_WIDTH, MATRIX_HEIGHT = SCREEN_SIZE
MATRIX_SIZE = MATRIX_WIDTH * MATRIX_HEIGHT

# Where to find the LED screen.
LED_SCREEN_ADDRESS = '10.0.5.184:7890'

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

# Zulip python client by the good zulip-people.
# Handles the polling (gets a callback) which is blocking
# Also message sending etc
zulipClient = zulip.Client(email=ZULIP_USERNAME,
                           api_key=API_KEY)
zulipRequestHandler = ZulipRequestHandler.ZulipRequestHandler(zulipClient,
                                                              ZULIP_USERNAME,
                                                              SCREEN_SIZE)
# opcClient is the Open Pixel Control client
# which provides the drivers (using LEDscape) an API to the LED-screen
opcClient = opc.Client(LED_SCREEN_ADDRESS)

_SCREEN_LOCK = Lock()
 
# Thanks Tristan!
# Call Zulip API to get a list of all streams.
def get_content():
    getter = requests.get('https://api.zulip.com/v1/streams', auth=requests.auth.HTTPBasicAuth(ZULIP_USERNAME, API_KEY))
    if getter.status_code == 200:
        return getter._content
    elif getter.status_code == 401:
        raise('check yo auth')
    else:
        raise(':( we failed to GET streams.\n(%s)' % getter)

# The Zulip-bot needs to subscribe to threads
# in order to receive messges
def subscribe_to_threads(zulipClient):
    _content = json.loads(get_content())     
    streams = _content['streams']
    stream_names = [stream['name'] for stream in streams]
     
    # Add subscriptions to bot
    streams = [{"name": str_name} for str_name in stream_names]
    zulipClient.add_subscriptions(streams)

# Puts the image on the screen.
# In this case image = pillow image object (might be image of text)
def showImage(image, x_offset=0, y_offset=0):
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
    opcClient.put_pixels(my_pixels, channel=0)


# Scroll image for frame_count through the screen.
# frame-count is in almost all cases just image width + screen width.
def scroll_message(image, frame_count):

    _SCREEN_LOCK.acquire()

    max_x_offset = image[0].size[0] + 1
    frame = 0
    counter = 0

    for i in xrange(max_x_offset + MATRIX_WIDTH):
        print("Showing image at offset %s frame %s / %s" % (i, frame, frame_count))
        time.sleep(1.0 / 60)
        showImage(image[frame], x_offset=i - MATRIX_WIDTH)
        counter = counter % 5
        if counter == 0:
            # for animated GIFs
            # if image has multiple frames change frame on every 5th scroll step
            frame = (frame + 1) % (frame_count)
        counter += 1

    _SCREEN_LOCK.release()


def handle_message(msg):
    # This will have to do ALL actions for the main loop.
    # Queue incoming messages
    # Check queue for the next message
    # Process that message
    # Show it to the screen
    #   - manage the displayed frames / scrolling etc
    if zulipRequestHandler.isBotMessage(msg):
        queue_token = zulipRequestHandler.get_msg_queue_token(msg)
        messageQueue.enqueue(queue_token)

    # TODO - ADD TIMER / FRAME COUNTER
    if not messageQueue.isEmpty():
        nextMsg = messageQueue.dequeue()

        # Display of message needs to happen in its own thread
        # to avoid blocking the message read process. If not done,
        # messages sent to bot during display activity would be ignored.
        thread = Thread(target=scroll_message, args=(nextMsg["image"], nextMsg["frame_count"]))
        thread.daemon = False
        thread.start()


def main():
    # running / blocking task
    # gets messages from messageQueue
    print('Trying to connect to LED-display...')
    if opcClient.can_connect():
        print('connected to %s' % LED_SCREEN_ADDRESS)
    subscribe_to_threads(zulipClient)

    print("Bot running... ")
    # Blocking call to zulip bot
    zulipClient.call_on_each_message(handle_message)

main()
