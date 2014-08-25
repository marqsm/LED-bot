import messageQueue as MessageQueue
import zulipRequestHandler as ZulipRequestHandler
import zulip
import opc

# LED Screen
MAX_FRAME_COUNT = 100
SCREEN_SIZE = (64, 32)
MATRIX_WIDTH, MATRIX_HEIGHT = SCREEN_SIZE
MATRIX_SIZE = MATRIX_WIDTH * MATRIX_HEIGHT
LED_SCREEN_ADDRESS = '10.0.5.184:7890'
messageXOffset = 0
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
# TODO: reading position from image xOffset, yOffset
def showImage(image, imageWidth, imageHeight, xOffset=0, yOffset=0):
    # Test if it can connect
    my_pixels = []

    for i in xrange(0, MATRIX_SIZE):
        x = i % MATRIX_WIDTH
        y = int(i / MATRIX_WIDTH)
        a = None
        if (x < imageWidth) and (y < imageHeight):

            r, g, b = image.getpixel((x, y))
            #if a == 0:
            #    r, g, b = 0, 0, 0
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
        imageWidth, imageHeight = nextMsg["image"].size
        showImage(nextMsg["image"], imageWidth, imageHeight)
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
