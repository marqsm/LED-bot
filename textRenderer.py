import colorsys
from PIL import Image, ImageFont, ImageDraw


class TextRenderer:

    def __init__(self, height=16, width=64, font="./NotoSansCJK-Bold.otf",
                 font_color=(0, 120, 0), color_bg=False):
        self.image = None

        # params
        self.screen_height = height
        self.screen_width = width
        self.color_bg = color_bg
        self.font_color = font_color
        self.text_to_send = " "
        self.color_cnt = 0

        # sizing set to 0
        self.total_width = 0
        self.msg_width = 0
        self.msg_height = 0
        self.single_msg_width = 0
        # TODO: count this from message pixel width.
        self.frame_count = 100

        # new image and font
        self.font = ImageFont.truetype(font, 24)
        self.im = Image.new("RGB", (self.screen_width, self.screen_height), "black")
        self.draw = ImageDraw.Draw(self.im)
        return None

    def getFrameCount(self):
        return self.frame_count

    def rainbow_bg(c):
        # hue, lightness, saturation to rgb
        vals = colorsys.hls_to_rgb(round(c / 360.0, 2), 0.05, 1)
        return (int(vals[0] * 255), int(vals[1] * 255), int(vals[2] * 255))

    def text_from_list(self, in_list):
        return "  ".join(in_list)

    def text_format(self, to_text):
        gap = "   "
        if len(to_text) > 1:
            return to_text + gap + to_text + gap
        else:
            return "Nice try, you sent an empty string.   Nice try, you sent an empty string.   "

    def make_message(self, my_list):
        self.text_to_send = self.text_format(unicode(self.text_from_list(my_list), 'UTF-8'))
        self.msg_width, self.msg_height = self.font.getsize(self.text_to_send)

        self.single_msg_width = int(self.msg_width / 2)
        self.total_width = self.msg_width + self.screen_width

    def draw_text(self, offset):
        self.im.paste((0, 0, 0), (0, 0, self.screen_width, self.screen_height))
        self.draw.text((self.screen_width - offset, 0), self.text_to_send,
                       font=self.font, fill=self.font_color)

    def render(self, msgText):
        _text = []
        print("TextRenderer.render", msgText);
        for word in msgText:
            if isinstance(word, unicode):
                word = str(word)
            _text.append(word)
        self.make_message(_text)

        # Should return the object we're going to queue
        # {
        #    iamge: pillowImage,
        #    action: "scroll",
        #    amount_of_frames: x
        # }
        #
        return None

    def getImage(self):
        return self.image

    def get_queue_token(self, msgToken):
        queue_token = {}
        # TODO: add possible params
        image = self.render(msgToken["text"])
        queue_token["image"] = image
        queue_token["frame_count"] = self.getFrameCount()
        queue_token["action"] = "scroll"
        queue_token["valid"] = True

        return queue_token
