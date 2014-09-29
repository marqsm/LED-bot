import pickle
from os.path import dirname, exists, join
import re

HERE = dirname(__file__)
class Emoji():

    def __init__(self):
        self.emoji_directory = dict()
        self._pickle_path = join(HERE, 'emoji-dict.pickle')
        self.init()

    def init(self):
        if exists(self._pickle_path) and self.load(self._pickle_path):
            print("Emoji dictionary ready.")

        else:
            self.create_dict(self.load_emoji_names())
            self.dump(self._pickle_path)
            print("Created new pickle file with emoji dictionary.")

    def load_emoji_names(self):
        with open(join(HERE, 'emoji.txt')) as f:
            return f.read().splitlines()

    def create_dict(self, emoji_names):
        emoji_d = dict()
        for emoji in emoji_names:
            emoji_img = emoji.strip(':') + ".png"
            emoji_d[emoji] = join(HERE, 'emoji',emoji_img)

        self.emoji_directory = emoji_d

    def load(self, filename):
        with open(filename, "rb") as f:
            try:
                self.emoji_directory = pickle.load(f)
                print("Pickle load was successful.")
                return True
            except:
                print("Loading emoji dictionary failed.")
                return False

    def dump(self, filename):
        try:
            with open(filename, "w+") as f:
                pickle.dump(self.emoji_directory, f)
                print("Pickle dump was successful.")
                return True
        except:
            print("Could not dump.")
            return False

    def check_emoji(self, emoji_name):
        # pattern to match emoji
        pattern = "^:[a-zA-Z0-9_]*:$"
        return re.match(pattern, emoji_name)
