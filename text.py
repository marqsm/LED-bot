import time
import random
import opc
from PIL import Image,ImageFont,ImageDraw

screen_width = 32*2
screen_height = 16

font = ImageFont.truetype("/Library/Fonts/comic.ttf",12)
my_text = "HACKER SCHOOL, NEVER GRADUATE!"
message_width, message_height = font.getsize(my_text)
ADDRESS = '10.0.5.184:7890'
client = opc.Client(ADDRESS)
while True:
	for i in range(message_width+screen_width/2):
		im = Image.new("RGB",(screen_width,screen_height),"black")
		draw = ImageDraw.Draw(im)

		print i
		draw.text((64-i,0), my_text, font=font)
		all_pixels = []
		pixels = im.load()
		img_width,img_height = im.size
		for y in range(screen_height):
			for x in range(screen_width):
				all_pixels.append(pixels[x,y])
		client.put_pixels(all_pixels, channel=0)
		time.sleep(0.05)
#im.show()