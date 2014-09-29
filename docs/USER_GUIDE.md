User Guide
----

### Zulip

LEDBot is accessible over Zulip. You can send LEDbot a private message or post one of these commands to a public channel

| command                              | parameters         | 
| ------------------------------------ | ------------------ |
| ```led-bot show-image <imagename>``` | image needs to be on the same server & directory where bot is running.  |
| ```led-bot show-text <text>```       | maximum of [1000](https://github.com/marqsm/LED-bot/blob/master/textRenderer.py#L12) characters  |


### HTTP API (POST)

You can send messages and images to LEDBot over HTTP!

| end point                            | parameters         |
| ------------------------------------ | ------------------ |
| ```http://host:4000/show-image/```    | url=image url  |
| ```http://host:4000/show-text/```     | message=your_text&r=100&g=0&b=0  |

### JSON Feeds

LEDBot can periodically pull data from arbitrary JSON feeds (ex, weather, quotes, news articles) and add them to the queue. This functionality is still rough and in development see `webFillerHandler.py`