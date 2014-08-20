#!/usr/bin/env python
# coding=UTF-8
import time
import opc
import zulip
import re
from marquee import Marquee_Text, Marquee_Data_Helpers
from PIL import Image
import urllib2 as urllib
from cStringIO import StringIO
# import requests
# import os

ZULIP_USERNAME = "led-bot@students.hackerschool.com"
# API_KEY in file named API_KEY
api_file = open('API_KEY', 'r')
API_KEY = api_file.read()
LED_SCREEN_ADDRESS = '10.0.5.184:7890'

# Prefix to recognize if a message is meant for the bot
BOT_MSG_PREFIX = '^(\\@\\*\\*)*led-bot(\\*\\*)*'

# Globals - sorry about that...
zulipClient = zulip.Client(email=ZULIP_USERNAME, api_key=API_KEY)
marq = Marquee_Text()
data_helper = Marquee_Data_Helpers()


class LedScreen:
    def __init__(self, address):
        self.matrixWidth = 64
        self.matrixHeight = 16
        self.matrix_size = self.matrixWidth * self.matrixHeight
        self.ADDRESS = address
        self.opcClient = opc.Client(self.ADDRESS)
        self.textXOffset = 0
        print('Trying to connect to LED-display...')
        if self.opcClient.can_connect():
            print('connected to %s' % self.ADDRESS)

    def loadImage(self, url):
        print('loadImage %s' % url)
        image_load_ok = None
        try:
            print('open url ' + url)
            img_file = urllib.urlopen(url)
            print('read file')
            im = StringIO(img_file.read())
            print 'open'
            self.image = Image.open(im)
            print 'load'
            self.image.load()
            print 'verify'
            # self.image.verify()
            print 'ok'
            image_load_ok = True
            # self.image = Image.open(filename)
            #file = cStringIO.StringIO(urllib.urlopen(URL).read())
            #self.image = Image.open(file)
            self.imageWidth, self.imageHeight = self.image.size
            print 'convert'
            self.image = self.image.convert('RGBA')
            print("Image loaded: ")
            print(self.image.format, self.image.size, self.image.mode, self.image.info)
        except:
            image_load_ok = False
            print("unable to load image")

        return image_load_ok

    def showImage(self):
        # Test if it can connect
        my_pixels = []

        for i in xrange(0, self.matrix_size):
            x = i % 64
            y = int(i / 64)
            a = None
            if (x < self.imageWidth) and (y < self.imageHeight):

                r, g, b, a = self.image.getpixel((x, y))
                if a == 0:
                    r, g, b = 0, 0, 0
                my_pixels.append((b, g, r))
            else:
                my_pixels.append((0, 0, 0))

        # dump data to LED display
        self.opcClient.put_pixels(my_pixels, channel=0)

    def cmdShowImage(self, userParams):
        if self.loadImage(userParams[0]):
            self.showImage()
        else:
            print "Image load failed."
            return False
            # TODO - add notification to the message that gets se

    # Show text in
    def cmdShowText(self, text):
        # text-parameter currently ignored
        print "cmdShowText %s" % (text)

        # Very stupid decoding of UTF-8 to default string format (ASCII?)
        # A hack to fix the message passing to marquee. There's probably a better way, like fixing this in marquee or something..

        _text = []
        for word in text:
            if isinstance(word, unicode):
                word = str(word)
            _text.append(word)
        # marq.make_message(["Never Graduate",data_helper.get_time(),"I'm a teapot","does this really work?","Maybe this message will display properly!"])
        marq.make_message(_text)

        while 1:
            # Loop drawing one frame
            if marq.time_to_reloop(self.textXOffset):
                self.textXOffset -= marq.msg_width
            else:
                self.textXOffset += 1

            print "Iteration: %s" % (self.textXOffset)
            marq.draw_text(self.textXOffset)

            self.opcClient.put_pixels(marq.slice_pixels(), channel=0)
            time.sleep(0.02)

    def runCommand(self, command, params):
        print("runCommand ", command, params)
        commands = {
            'show-image': self.cmdShowImage,
            'show-text': self.cmdShowText
        }

        if command in commands:
            return commands.get(command)(params)
        else:
            print("Command '%s' not found - params: %s " % (command, params))


def isBotMessage(senderEmail, msgContent):
    # Check that bot is not talking to itself and message is meant for the bot
    if (senderEmail != ZULIP_USERNAME
            and (re.match(BOT_MSG_PREFIX, msgContent, flags=re.I or re.X))):
        return True
    return False


# Get response object for user sent message
def getResponseContent(msg):
    if msg["type"] == "stream":
        # user message was public
        msgTo = msg["display_recipient"]    # name of the stream
    elif msg["type"] == "private":
        # message sent by user is a private stream message
        msgTo = msg["sender_email"]

    msgText = """JUST GIVE ME A SEC I'LL SHOW YOUR STUFF WHEN I HAVE THE TIME
                WE'RE ALL UNDER A LOT OF PRESSURE HERE!!!"""
    resp = {
        "type": msg["type"],
        "subject": msg["subject"],              # topic within the stream
        "to": msgTo,                             # name of the stream
        "content": "%s" % msgText               # message to print to stream
    }

    return resp


# Parse user-sent input string to
def getCommandAndParams(content):
    # TODO : functionality
    cmdAndParams = re.sub(BOT_MSG_PREFIX, '', content).split()
    print('getCommandAndParams: ', cmdAndParams)
    return cmdAndParams[0], cmdAndParams[1:]


# call respond function when zulipClient interacts with gif bot
def respond(msg):
    # Check if message is meant for the bot
    if isBotMessage(msg['sender_email'], msg['content']):
        resp = getResponseContent(msg)
        server_response = zulipClient.send_message(resp)
        print(resp)
        print(server_response)

        screen = LedScreen(LED_SCREEN_ADDRESS)
        command, params = getCommandAndParams(msg['content'])
        command_successful = screen.runCommand(command, params)

        # puts messages sent by bot to stack to enable undo functionality
        # TODO: Push undo-message to queue.
        # TODO: If isUndo(msg) pop the latest message, create undo to LED


def main():
    # Get subscriptions to existing streams.
    # TODO: Fetch subscriptions dynamically
    f = open('subscriptions.txt', 'r')

    ZULIP_STREAM_SUBSCRIPTIONS = []
    try:
        for line in f:
            ZULIP_STREAM_SUBSCRIPTIONS.append(line.strip())
    finally:
        f.close()

    # Add subscriptions to bot
    zulipClient.add_subscriptions([{"name": stream_name} for stream_name in ZULIP_STREAM_SUBSCRIPTIONS])

    # This is a blocking call that will run forever, keepalive loop for the bot
    print("Bot running... ")
    zulipClient.call_on_each_message(respond)

main()
