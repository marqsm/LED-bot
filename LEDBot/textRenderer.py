# Standard library
from os.path import abspath, dirname, join

# 3rd party library
from PIL import Image, ImageFont, ImageDraw
import emojiHandler as EmojiHandler
import imageRenderer as ImageRenderer

# LED Screen physical dimensions
MAX_FRAME_COUNT = 100
SCREEN_SIZE = (64, 32)
MATRIX_WIDTH, MATRIX_HEIGHT = SCREEN_SIZE
MATRIX_SIZE = MATRIX_WIDTH * MATRIX_HEIGHT

FONT_DIR = join(abspath(dirname(__file__)), 'fonts')
DEFAULT_FONT = join(FONT_DIR, 'NotoSansCJK-Bold.otf')

class TextRenderer:

    def __init__(self, font=DEFAULT_FONT, font_color=(0, 120, 0),
                 bg_color=(0, 0, 0)):

        # params
        self.default_bg_color = bg_color
        self.default_font_color = font_color
        self.MAX_TEXT_LENGTH = 1000

        # new image and font
        self.font = ImageFont.truetype(font, 22)

        # Emoji Handler
        self.emoji_handler = EmojiHandler.Emoji()

        # ImageRenderer
        self.image_renderer = ImageRenderer.ImageRenderer(SCREEN_SIZE)

    def draw_text(self, text_to_send, text_color=None, bg_color=None):
        text_to_send = self.truncate_text(text_to_send)
        x, y = self.font.getsize(text_to_send)

        if text_color is None:
            text_color = self.default_font_color

        if bg_color is None:
            bg_color = self.default_bg_color

        # Add padding below, because PIL sucks!
        image = Image.new("RGB", (x, y+10), bg_color)

        ImageDraw.Draw(image).text(
            (0, 0), text_to_send, font=self.font, fill=text_color
        )

        return image

    def pre_draw(self, text, text_color=None, bg_color=None):
        sentence = []
        for x in text:
            # check if x is emoji, AND if emoji exists in the emoji dictionary
            if self.emoji_handler.check_emoji(x) and x in self.emoji_handler.emoji_directory:
                url = self.emoji_handler.emoji_directory[x]
                img = self.image_renderer.fetch_image(url)
                new_size = self.image_renderer.get_new_size(img, SCREEN_SIZE[0], SCREEN_SIZE[1])
                img = img.convert("RGB").resize(new_size)
                sentence.append(img)
            else:
                sentence.append(self.draw_text(" " + x, text_color, bg_color))

        return sentence

    def concat_images(self, tokens):
        total_width = 0
        height = tokens[0].size[1]
        for slide in tokens:
            total_width += slide.size[0] + 1

        new_image = Image.new("RGB", (total_width, height))

        x_offset = 0

        for slide in tokens:
            new_image.paste(slide, (x_offset, 0))
            x_offset += slide.size[0] + 1

        return new_image

    def get_queue_token(self, msgToken):
        queue_token = {}
        pre_draw = self.pre_draw(msgToken['text'], msgToken.get('color', None),
            msgToken.get('background-color', None))
        # TODO: add possible params
        queue_token['image'] = [self.concat_images(pre_draw)]

        queue_token["frame_count"] = 1
        queue_token["action"] = "scroll"
        queue_token["valid"] = True

        return queue_token

    def truncate_text(self, text_to_send):
        return text_to_send[:self.MAX_TEXT_LENGTH]
