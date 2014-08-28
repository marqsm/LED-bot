import urllib2 as urllib
from cStringIO import StringIO
from PIL import Image, ImageSequence
import re
# This componenets gets a URL for an image
# returns a queue token with that PILLOW image
# resizes and converts to RGBA and splits animated images to frames


class ImageRenderer:

    def __init__(self, screenSize):
        self.screenSize = screenSize

    # calculates size for image that fits new resolution
    # without changing image aspect ratio
    def get_new_size(self, image, screen_width, screen_height):
        # returns new image h/w to fit screen
        img_width, img_height = image.size
        img_ratio = img_width / img_height
        screen_ratio = screen_width / screen_height
        if screen_ratio > img_ratio:
            return (img_width * screen_height / img_height, screen_height)

        else:
            return (screen_width, img_height * screen_width / img_width)

    # Get remote image, return image object
    def fetch_image(self, url):
        print('loadImage %s' % url)

        try:
            img_file = urllib.urlopen(url)
            headers = img_file.info()
            # if size under 2MB and matches image type in header
            if int(headers['Content-Length']) < 2000000 and re.match(r"image",headers['Content-Type']):
                im = StringIO(img_file.read())
                image = Image.open(im)
                image.load()
            else:
                image = None
        except:
            print("Print fetching the image failed")
            image = None

        return image

    # form queue token from message token
    def get_queue_token(self, msgToken):
        print("get_queue_token got an msgToken")
        print(msgToken)
        # TODO: add possible params
        image = self.fetch_image(msgToken["url"])
        return self._get_queue_token_from_image(image) if image is not None else None


    # do image processing needed for queue token
    def _get_queue_token_from_image(self, image):
        queue_token = {}
        new_size = self.get_new_size(image, self.screenSize[0], self.screenSize[1])
        images = [
            frame.convert("RGBA").resize(new_size)

            for frame in ImageSequence.Iterator(image)
        ]

        queue_token["image"] = map(self._get_black_background_images, images)
        queue_token["frame_count"] = len(images)
        queue_token["action"] = "scroll"
        queue_token["valid"] = True

        return queue_token

    def _get_black_background_images(self, image):
        """Create black background images from transperent images.

        The images here are expected to be RGBA. Sending RGB images wouldn't
        make much sense.

        """

        bg = Image.new("RGB", image.size, (0, 0, 0))
        bg.paste(image, image)

        return bg
