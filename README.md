LED Bot
=========

[![Documentation Status](https://readthedocs.org/projects/led-bot/badge/?version=latest)](https://readthedocs.org/projects/led-bot/?badge=latest)

![marquee](./docs/marquee.gif)

LEDBot is a scheduler and application server. You can use it to stream images, messages, emoji and more to LED message displays in
your home, office, school or hacker space.

At the moment LEDbot can accept input from
[Hacker School's](https://hackerschool.com) internal chat system, Zulip, a web front-end and API, IRC and fetch arbitrary JSON feeds. It shouldn't be difficult to add other types of input (SMS, Slack,
etc). [Take a look at the code](https://github.com/marqsm/LED-bot/blob/master/LEDBot/bot_scheduler.py#L252)
and write another listener!

[![Emoji in LED form](http://img.youtube.com/vi/J9WWJnb6t8M/0.jpg)](http://www.youtube.com/watch?v=J9WWJnb6t8M)

Currently pipeline is working, supports these commands.

#### Zulip

| command                              | parameters         |
| ------------------------------------ | ------------------ |
| ```led-bot show-image <image-url>``` | An image url  |
| ```led-bot <text>```       | maximum of [1000](https://github.com/marqsm/LED-bot/blob/master/textRenderer.py#L12) characters  |

#### HTTP

A simple browser-based front-end is available at ```http://host:4000/```. Text and images can be sent via POST requests to API end points.

| end point                             | parameters         |
| ------------------------------------  | ------------------ |
| ```http://host:4000/```    			| browser-based front-end |
| ```http://host:4000/show-image/```    | url=image url  |
| ```http://host:4000/show-text/```     | message=your_text&color=255,0,0  |

#### IRC

Message or mention LEDbot with the following

| command                            | Details         |
| ------------------------------------  | ------------------ |
| ```show <text>```    					| Displays given text  |
| ```img <url>```     					| Displays image at given url  |
| ```color <r> <g> <b>```     					| Sets text color  |

### JSON Feeds

LEDBot can periodically pull data from arbitrary feeds (ex: weather, quotes, news articles) and add them to the queue. This functionality is still rough and in development see `webFillerHandler.py`


Output is [Open Pixel Control](http://openpixelcontrol.org/).

LEDBot uses
[NYC Resistor's](http://www.nycresistor.com/2013/09/12/octoscroller/)
[LEDscape](https://github.com/osresearch/LEDscape) as our low-level interface and a [Noto Font](https://code.google.com/p/noto/) to support Latin, Cyrillic, Japanese, Chinese and Korean character sets.

## Installation instructions

The documentation for the project is on
[Read the docs](http://led-bot.readthedocs.org/en/latest/)

## Goals

This project aims to be AWESOME to contribute to, especially for new Hacker
Schoolers.  To begin contributing, look at the long list of
[issues](https://github.com/marqsm/LED-bot/issues) we have!

## Authors

Created at [Hacker School](https://hackerschool.com), Summer 2014
