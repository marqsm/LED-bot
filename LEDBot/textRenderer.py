# Standard library
from os.path import abspath, dirname, join

# 3rd party library
from PIL import Image, ImageFont, ImageDraw

FONT_PATH = abspath(dirname(__file__))
DEFAULT_FONT = join(FONT_PATH, 'NotoSansCJK-Bold.otf')

class TextRenderer:

    def __init__(self, font=DEFAULT_FONT, font_color=(0, 120, 0),
                 color_bg=(0, 0, 0)):

        # params
        self.default_color_bg = color_bg
        self.default_font_color = font_color
        self.MAX_TEXT_LENGTH = 1000

        # new image and font
        self.font = ImageFont.truetype(font, 22)

    def draw_text(self, text_to_send, text_color=None, bg_color=None):
        text_to_send = self.truncate_text(text_to_send)
        x, y = self.font.getsize(text_to_send)

        if text_color is None:
            text_color = self.default_font_color

        if bg_color is None:
            bg_color = self.default_color_bg

        # Add padding below, because PIL sucks!
        image = Image.new("RGB", (x, y+10), text_color)

        ImageDraw.Draw(image).text(
            (0, 0), text_to_send, font=self.font, fill=bg_color
        )

        return image

    def get_queue_token(self, msgToken):
        queue_token = {}
        # TODO: add possible params
        queue_token['image'] = [self.draw_text(
            ' '.join(msgToken['text']),
            msgToken.get('color', None),
            msgToken.get('background-color', None)
        )]

        queue_token["frame_count"] = 1
        queue_token["action"] = "scroll"
        queue_token["valid"] = True

        return queue_token

    def truncate_text(self, text_to_send):
        return text_to_send[:self.MAX_TEXT_LENGTH]
