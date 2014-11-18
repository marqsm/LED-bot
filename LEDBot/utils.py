from ConfigParser import ConfigParser
from os.path import expanduser, exists


CONFIG_PATH = expanduser('~/.led-bot.conf')

def create_config_file():
    print('Config file does not exist. Creating one!')
    with open(CONFIG_PATH, 'w') as f:
        config = ConfigParser()
        
        # opc socket
        config.add_section('main')
        config.set('main', 'led_screen_address', 'localhost:7890')

        # zulip info
        config.add_section('zulip')
        config.set('zulip', 'username', 'led-bot@students.hackerschool.com')
        config.set('zulip', 'API_KEY', raw_input('Zulip API_KEY: ').strip())

        # http server
        config.add_section('http')
        config.set('http', 'host', '0.0.0.0')
        config.set('http', 'port', '4000')

        # irc chat
        config.add_section('irc')
        config.set('irc', 'host', 'chat.freenode.net')
        config.set('irc', 'port', '6667')
        config.set('irc', 'channel', '#ledbot')
        config.set('irc', 'nick', 'ledbot123')

        # web fillers
        config.add_section('fillers')
        config.set('fillers', 'time_interval', '200.0')

        # mqtt
        config.add_section('mqtt')
        config.set('mqtt', 'host', 'test.mosquitto.org')
        config.set('mqtt', 'port', '1883')
        config.set('mqtt', 'channel', 'ledbot/')
        config.set('mqtt', 'user', '')
        config.set('mqtt', 'pass', '')

        config.write(f)


def get_config():
    if not exists(CONFIG_PATH):
        create_config_file()

    with open(CONFIG_PATH) as f:
        config = ConfigParser()
        config.readfp(f)
        return config
