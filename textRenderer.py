from PIL import Image, ImageFont, ImageDraw


class TextRenderer:

    def __init__(self, font="./NotoSansCJK-Bold.otf",
                 font_color=(0, 120, 0), color_bg=(0, 0, 0)):

        # params
        self.default_color_bg = color_bg
        self.default_font_color = font_color
        self.MAX_TEXT_LENGTH = 1000
        
        # new image and font
        self.font = ImageFont.truetype(font, 22)
        
    def draw_text(self, text_to_send, text_color, bg_color):
        text_to_send = self.truncate_text(text_to_send)
        x, y = self.font.getsize(text_to_send)
        
        if not text_color:
            text_color = self.default_font_color
        
        if not bg_color:
            bg_color = self.default_color_bg

        # Add padding below, because PIL sucks!
        image = Image.new("RGBA", (x, y+10), text_color)

        ImageDraw.Draw(image).text(
            (0, 0), text_to_send, font=self.font, fill=bg_color
        )

        return image

    def get_queue_token(self, msgToken):
        queue_token = {}
        # TODO: add possible params
        queue_token["image"] = [self.draw_text(' '.join(msgToken["text"], msgToken["color"], msgToken["background-color"]))]
        queue_token["frame_count"] = 1
        queue_token["action"] = "scroll"
        queue_token["valid"] = True

        return queue_token
    
    def truncate_text(self, text_to_send):
        return text_to_send[:self.MAX_TEXT_LENGTH]
