import urllib
import StringIO
from PIL import Image


class ImageRenderer:

    def __init__(self, screenSize):
        self.image = None
        self.screen_width, self.screen_height = screenSize
        self.screen_ratio = screen_width / self.screen_height 

    def convert_image(self, image):
        # TODO: converion
        # TODO: error, if conversion fails
        try:
            rgb_image = image.convert("RGBA")
        except:
            "unable to convert image to RGBA format"
            return False

        return rgb_image

    def resize_image(self,img_width,img_height):
        # returns new image h/w to fit screen
        img_ratio = img_width / img_height
        if self.screen_ratio > img_ratio:
            return (img_width * self.screen_height / img_height , screen_height)
        else:
            return (self.screen_width, img_height * self.screen_width / img_width)

    def get_frames(self):
        # cycle through and return rendered frames, handles animated images
        frames = []
        while 1:
            try:
                self.image.seek(self.image.tell()+1)
                frame.append(self.image.convert("RGB"))
            except EOFError:
                return frames

    def fetch_image(self, url):
        print('loadImage %s' % url)
        image_load_ok = None
        try:
            img_file = urllib.urlopen(url)
            im = StringIO(img_file.read())
            self.image = Image.open(im)
            self.image.load()
            print 'verify'
            # self.image.verify()
            # image_load_ok = True
        except:
            print("Print fetching the image failed")
        # image = None
        # TODO : fetch remote image
        return self.image

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
