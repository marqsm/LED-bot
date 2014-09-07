Development Guide
----

We welcome contributors from within and outside of Hacker School. Let's make LEDbot amazing!

### Setup Your Development Environment

Theres many ways to dev this locally, but heres one recommendation


- Install virtualenv

- Create a new virtualenv for the bot

    ```
    virtualenv ~/.pythons/ledbot
    ```

- Activate the virtualenv 
    
    ```
    source ~/.pythons/ledbot/bin/activate
    ````

- Install the dependencies and the LED-bot source in development mode. 

    ```
    python setup.py develop
    ````

- You can get an API key from your zulip account

- Run the bot

    ```
    python LEDBot/bot_scheduler.py
    ```

- Run the simulator (make sure your config specifies localhost:7890)

    ```
    python LEDBot/simulator.py
    ```

- If you wish to change the config, edit the file `~/.led-bot.conf`


### Notes On Architecture

At the moment our application accepts input from our internal chat system, Zulip, but it shouldn't be too hard to add other types of input (SMS, IRC, Slack, Web, etc) [take a look at the code here](https://github.com/marqsm/LED-bot/blob/master/LEDBot/bot_scheduler.py#L252) and write another listener!

Output is Open Pixel Control, so the software should operate with a variety of LED installations.

| file                  | purpose           | 
| --------------------- | ------------------|
| bot_scheduler.py      | The main, handles displaying and scrolling text on the screen                     |
| textRenderer.py       | Where the image for text gets created. Things like text colors and style, image pre-processing go here        |
| imageRenderer.py      | Where the images get processed                |
| opc.py                | Open Pixel Control handler                    |
| zulipRequestHandler.py| handle Zulip tasks                            |


![arch](https://raw.githubusercontent.com/marqsm/LED-bot/master/docs/architecture.png)

