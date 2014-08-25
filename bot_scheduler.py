import messageQueue as MessageQueue
import zulipRequestHandler as ZulipRequestHandler
import zulip
import opc
import time

# LED Screen
MAX_FRAME_COUNT = 100
SCREEN_SIZE = (64, 32)
MATRIX_WIDTH, MATRIX_HEIGHT = SCREEN_SIZE
MATRIX_SIZE = MATRIX_WIDTH * MATRIX_HEIGHT
LED_SCREEN_ADDRESS = '10.0.5.184:7890'
messagex_offset = 0
currentFrameCount = 0

# Zulip Conf
ZULIP_USERNAME = "led-bot@students.hackerschool.com"
api_file = open('API_KEY', 'r')
API_KEY = api_file.read()

# Components
messageQueue = MessageQueue.MessageQueue()


zulipClient = zulip.Client(email=ZULIP_USERNAME,
                           api_key=API_KEY)
zulipRequestHandler = ZulipRequestHandler.ZulipRequestHandler(zulipClient,
                                                              ZULIP_USERNAME,
                                                              SCREEN_SIZE)
opcClient = opc.Client(LED_SCREEN_ADDRESS)


def init():
    return None


def show_frame():
    # puts the image to the LED display
    return None


def subscribe_to_threads(zulipClient):
    f = open('subscriptions.txt', 'r')

    ZULIP_STREAM_SUBSCRIPTIONS = []
    try:
        for line in f:
            ZULIP_STREAM_SUBSCRIPTIONS.append(line.strip())
    finally:
        f.close()

    # Add subscriptions to bot
    streams = [{"name": str_name} for str_name in ZULIP_STREAM_SUBSCRIPTIONS]
    zulipClient.add_subscriptions(streams)


# Puts the image on the screen
# TODO: reading position from image x_offset, y_offset
def showImage(image, x_offset=0, y_offset=0):
    # Test if it can connect
    print("Image size", image.size)
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


def show_message():
    # Handles the display of the whole message
    # This includes timing, scrolling, managing offsets

    # call render_text
    # call render_image

    # uses self.show_frame
    return False


# Scroll image for frame_count
def scroll_message(image, frame_count):
    max_x_offset = image[0].size[0] + 1
    frame = 0

    for i in xrange(max_x_offset + MATRIX_WIDTH):
        print("Showing image at offset %s frame %s / %s" % (i, frame, frame_count))
        time.sleep(1.0 / 60)
        showImage(image[frame], x_offset=i - MATRIX_WIDTH)
        frame = (frame + 1) % frame_count


def handle_message(msg):
    if zulipRequestHandler.isBotMessage(msg):
        queue_token = zulipRequestHandler.get_msg_queue_token(msg)
        messageQueue.enqueue(queue_token)

    # TODO - ADD TIMER / FRAME COUNTER
    if not messageQueue.isEmpty():
        print("handle_message from queue", queue_token)
        nextMsg = messageQueue.dequeue()
        print 'Dequed token ------------------------'
        print nextMsg
        scroll_message(nextMsg["image"], nextMsg["frame_count"])

        # TODO: Show it on the screen

    # This will have to do ALL actions for the main loop.
    # Queue incoming messages
    # Check queue for the next message
    # Process that message
    # Show it to the screen
    #   - manage the displayed frames / scrolling etc
    return None


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
