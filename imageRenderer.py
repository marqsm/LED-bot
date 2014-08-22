
class ImageRenderer:

    def __init__(self, screenSize):
        self.image = None
        self.screen_width, self.screen_height = screenSize
        self.screen_ratio = screen_width / self.screen_height 

    def render(msg):
        # Should return the object we're going to queue
        # {
        #    iamge: pillowImage,
        #    action: "scroll",
        #    amount_of_frames: x
        # }
        #
        return None

    def convert_image(self, image):
        # TODO: converion
        # TODO: error, if conversion fails
        try:
            rgb_image = image.convert("RGB")
        except:
            "unable to convert image to RGB format"
            return False

        return rgb_image

    def resize_image(self,img_width,img_height):
        # returns new image h/w to fit screen
        img_ratio = img_width / img_height
        if self.screen_ratio > img_ratio:
            return (img_width * self.screen_height / img_height , screen_height)
        else:
            return (self.screen_width, img_height * self.screen_width / img_width)


    def fetch_image(self, url):
        image = None
        # TODO : fetch remote image
        return image

    def get_queue_token(self, msgToken):
        queue_token = {}
        # TODO: add possible params
        image = self.render(msgToken["text"])
        queue_token["image"] = image
        queue_token["frame_count"] = self.getFrameCount(image)
        queue_token["action"] = "scroll"

        return queue_token

    def getImage(self):
        return self.image
