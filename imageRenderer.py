import urllib
import StringIO
from PIL import Image


class ImageRenderer:

    def __init__(self, screenSize):
        self.image = None
        self.width, self.height = screenSize

    def convert_image(self, image):
        # TODO: converion
        # TODO: error, if conversion fails
        try:
            rgb_image = image.convert("RGBA")
        except:
            "unable to convert image to RGBA format"
            return False

        return rgb_image

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
