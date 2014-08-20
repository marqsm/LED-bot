# Renderer class calls imageRenderer and textRender to get the actual frames.
# It returns the rendere-object:
# {
#    type: "text" | "image" ,
#    url: "(inage url if image",
#    text: "text if type == text"
# }
import textRenderer
import imageRenderer
from PIL import Image
import urllib2 as urllib
from cStringIO import StringIO
from marquee import Marquee_Text, Marquee_Data_Helpers


class Renderer:
    def __init__(self):
        self.imageObj = None
        self.frameCount = 0

    def renderText(self, text):
        self.imageObj = ""

    def renderImage(self, imageUrl):
        self.imageObj = ""

    def getImage(self):
        return self.imageObj
