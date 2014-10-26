LED Bot
=========

LEDBot is a scheduler and application server. You can use it to stream images, messages, emoji and more to LED displays in your home, office, school or hacker space.

#### Zulip

| command                              | parameters         |
| ------------------------------------ | ------------------ |
| ```led-bot show-image <image-url>``` | An image url  |
| ```led-bot <text>```       | maximum of [1000](https://github.com/marqsm/LED-bot/blob/master/textRenderer.py#L12) characters  |

#### HTTP (POST)

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

## Goals

This project aims to be AWESOME to contribute to, especially for new Hacker
Schoolers.  To begin contributing, look at the long list of
[issues](https://github.com/marqsm/LED-bot/issues) we have!

## Authors

Created at [Hacker School](https://hackerschool.com), Summer 2014
