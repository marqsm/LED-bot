User Guide
----

### Zulip

LEDBot is accessible over Zulip. You can send LEDbot a private message or post one of these commands to a public channel

| command                              | parameters         | 
| ------------------------------------ | ------------------ |
| ```led-bot show-image <imagename>``` | image needs to be on the same server & directory where bot is running.  |
| ```led-bot <text>```       | maximum of [1000](https://github.com/marqsm/LED-bot/blob/master/textRenderer.py#L12) characters  |


#### HTTP API

A simple browser-based front-end is available at ```http://host:4000/```. Text and images can be sent via POST requests to API end points.

| end point                             | parameters         |
| ------------------------------------  | ------------------ |
| ```http://host:4000/```    			| browser-based front-end |
| ```http://host:4000/show-image/```    | url=image url  |
| ```http://host:4000/show-text/```     | message=your_text&color=255,0,0  |

#### IRC

Message or mention LEDbot with the following. By default LEDBot joins a Freenode channel called #ledbot 

| command                            | Details         |
| ------------------------------------  | ------------------ |
| ```show <text>```    					| Displays given text  |
| ```img <url>```     					| Displays image at given url  |
| ```color <r> <g> <b>```     					| Sets text color  |

### MQTT

LEDBot can connect to a [MQTT](http://www.eclipse.org/paho/) broker and subscribe to channels for "push" notifications. This functionality is very minimal at the moment and can be expanded upon with additional parameters. By default LEDBot listens to channel `ledbot/` on the public broker `test.mosquitto.org`

### JSON Feeds

LEDBot can periodically pull data from arbitrary JSON feeds (ex, weather, quotes, transit times, news articles) and add them to the queue. This functionality is still rough and in development see `webFillerHandler.py`