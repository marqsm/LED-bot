import pickle
import os
import re

class Emoji():

    def __init__(self):
        self.emoji_directory = dict()
        self.init()

    def init(self):
        if os.path.exists("emoji-dict.pickle") and self.load("emoji-dict.pickle"):
            print("Emoji dictionary ready.")
        else:
            self.create_dict(self.load_emoji_names())
            self.dump("emoji-dict.pickle")
            print("Created new pickle file with emoji dictionary.")

    def load_emoji_names(self):
        f = open('emoji.txt', 'r')
        EMOJI_NAMES = []

        try:
            for line in f: 
                EMOJI_NAMES.append(line.strip())
        finally: 
            f.close()

        return EMOJI_NAMES

    def create_dict(self, EMOJI_NAMES): 
        emoji_d = dict()
        for emoji in EMOJI_NAMES:
            emoji_d[emoji] = "https://zulip.com/static/third/gemoji/images/emoji/%s.png" % emoji.strip(':')

        # special add the HS emoji
        emoji_d['hackerschool'] = "https://external-content.zulipcdn.net/1fd50dd9cd66190492ee5c1f \
        3c82b49a5f6fdf45/687474703a2f2f7765622e6d69742e6564752f6a657373746573732f7777772f7265616c6d656d6f \
        6a692f6861636b65727363686f6f6c2e706e67"

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