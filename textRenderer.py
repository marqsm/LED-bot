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

    def draw_text(self):
        # self.im.paste((0, 0, 0), (0, 0, self.screen_width, self.screen_height))
        size = self.font.getsize(self.text_to_send)

        self.im = Image.new("RGB", size, "black")
        self.draw = ImageDraw.Draw(self.im)

        self.draw.text((0, 0), self.text_to_send,
                       font=self.font, fill=self.font_color)

    def render(self, msgText):
        _text = []
        print("TextRenderer.render", msgText)
        for word in msgText:
            if isinstance(word, unicode):
                word = str(word)
            _text.append(word)
        self.text_to_send = ' '.join(_text)        # self.make_message(_text)
        self.draw_text()

        return None

    def getImage(self):
        return self.image

    def get_queue_token(self, msgToken):
        queue_token = {}
        # TODO: add possible params
        self.render(msgToken["text"])
        queue_token["image"] = self.im
        queue_token["frame_count"] = self.getFrameCount()
        queue_token["action"] = "scroll"
        queue_token["valid"] = True

        return queue_token
