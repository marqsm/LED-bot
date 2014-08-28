from PIL import Image, ImageFont, ImageDraw
import emojiHandler as EmojiHandler
import imageRenderer as ImageRenderer

# LED Screen physical dimensions
MAX_FRAME_COUNT = 100
SCREEN_SIZE = (64, 32)
MATRIX_WIDTH, MATRIX_HEIGHT = SCREEN_SIZE
MATRIX_SIZE = MATRIX_WIDTH * MATRIX_HEIGHT

class TextRenderer:

    def __init__(self, font="./NotoSansCJK-Bold.otf",
                 font_color=(0, 120, 0), color_bg=(0, 0, 0)):

        # params
        self.default_color_bg = color_bg
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
            bg_color = self.default_color_bg

        # Add padding below, because PIL sucks!
        image = Image.new("RGBA", (x, y+10), text_color)

        ImageDraw.Draw(image).text(
            (0, 0), text_to_send, font=self.font, fill=bg_color
        )

        return image

    def pre_draw(self, text, text_color=None, bg_color=None):
        sentence = []
        for x in text:
            if self.emoji_handler.check_emoji(x):
                url = self.emoji_handler.emoji_directory[x]
                img = self.image_renderer.fetch_image(url)
                new_size = self.image_renderer.get_new_size(img, SCREEN_SIZE[0], SCREEN_SIZE[1])
                img = img.convert("RGBA").resize(new_size)
                sentence.append(img)
            else:
                sentence.append(self.draw_text(" " + x, text_color, bg_color))

        return sentence

    def get_queue_token(self, msgToken):
        queue_token = {}
        # TODO: add possible params
        queue_token['image'] = [self.pre_draw(msgToken['text'],
            msgToken.get('color', None),
            msgToken.get('background-color', None)
        )]

        queue_token["frame_count"] = 1
        queue_token["action"] = "scroll"
        queue_token["valid"] = True

        return queue_token

    def truncate_text(self, text_to_send):
        return text_to_send[:self.MAX_TEXT_LENGTH]
