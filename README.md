LED Bot
=========

![marquee](./docs/marquee.gif)

A LED application server. Stream images, messages and more to LEDs in your home, office, hacker space.

Currently pipeline is working, supports to commands.

| command                              | parameters         |
| ------------------------------------ | ------------------ |
| ```led-bot show-image <imagename>``` | image needs to be on the same server & directory where bot is running.  |
| ```led-bot show-text <text>```       | maximum of [1000](https://github.com/marqsm/LED-bot/blob/master/textRenderer.py#L12) characters  |

## Installation instructions

The [hardware](https://github.com/marqsm/LED-bot/wiki/Build---Hardware) and
[software](https://github.com/marqsm/LED-bot/wiki/Build---Software)
installation instructions are on the
[Wiki](https://github.com/marqsm/LED-bot/wiki)


TODO:
See our issues page!

- Add possibility to move an image across the screen (like immobile pacman) - of course way cooler with animated gifs
- Errorhandling for image loading - now pretty weak
- Make a message queue for incoming messages
- Make some kind of scheduler to decide how long to show messages

DONE:
x Fix to support longer texts for "show-text"
x add support to animated gifs
x Add commands for sampling / scrolling images, if they are too big for the screen
x Hardware soldering
x fetch remote images (url)
x Figure out software dependencies on beagleBone for OpenPixel
x Learn OpenPixel file format
x Build Zulip bot
x Get communication from server to hardware
x Figure out conversion from raw data to OpenPixel format


Goal:

(done) 1. Reference app running from network to HW

2. AWESOMENESS!!!!!

APPLICATION DESIGN / DEV GUIDE

| file                  | purpose         	|
| --------------------- | ------------------|
| bot_scheduler.py		| The main, handles displaying and scrolling text on the screen 					|
| textRenderer.py		| Where the image for text gets created. Things like text colors and style, image pre-processing go here 		|
| imageRenderer.py  	| Where the images get processed				|
| MessageQueue.py  		| Message queue 								|
| opc.py 				| Open Pixel Control handler 					|
| zulipRequestHandler.py| handle Zulip tasks							|


![arch](./architecture.png)




Created at [Hacker School](https://hackerschool.com), Summer 2014
