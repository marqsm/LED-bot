from PIL import Image, ImageFont, ImageDraw


class TextRenderer:

    def __init__(self, font="./NotoSansCJK-Bold.otf",
                 font_color=(0, 120, 0), color_bg=False):

        # params
        self.color_bg = color_bg
        self.font_color = font_color
        # new image and font
        self.font = ImageFont.truetype(font, 22)

    def draw_text(self, text_to_send):
        x, y = self.font.getsize(text_to_send)

        # Add padding below, because PIL sucks!
        image = Image.new("RGBA", (x, y+10), "black")

        ImageDraw.Draw(image).text(
            (0, 0), text_to_send, font=self.font, fill=self.font_color
        )

        return image

    def get_queue_token(self, msgToken):
        queue_token = {}
        # TODO: add possible params
        queue_token["image"] = [self.draw_text(' '.join(msgToken["text"]))]
        queue_token["frame_count"] = 1
        queue_token["action"] = "scroll"
        queue_token["valid"] = True

        return queue_token
