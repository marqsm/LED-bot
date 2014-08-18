import time
import random
import opc
import colorsys
import sys
from PIL import Image,ImageFont,ImageDraw

# config stuff
screen_width = 32*2
screen_height = 16
target_address = '10.0.5.184:7890'
frame_delay = 0.03
font = ImageFont.truetype("/Library/Fonts/comic.ttf",14)
make_rainbows = True

# if argv 
def get_text():
	if sys.argv[1]:
		return sys.argv[1]
	else:
		return "HACKER SCHOOL, NEVER GRADUATE!"

#rainbow bg
def rainbow_bg(x,total):
	# hue, lightness, saturation to rgb 
	vals = colorsys.hls_to_rgb(round(float(x)/total,2),0.05,1)
	return (int(vals[0]*255),int(vals[1]*255),int(vals[2]*255))
	
my_text = get_text()	
message_width, message_height = font.getsize(my_text)

im = Image.new("RGB",(screen_width,screen_height),"black")
draw = ImageDraw.Draw(im)

total_width = message_width + screen_width

client = opc.Client(target_address)



while True:
	for i in range(total_width):
		if make_rainbows:
			bg = rainbow_bg(i,message_width)
		else:
			bg = (0,0,0)
		
		im.paste(bg, (0,0,screen_width,screen_height))
		draw.text((64-i,0), my_text, font=font)
		all_pixels = []
		pixels = im.load()
		img_width,img_height = im.size
		for y in range(screen_height):
			for x in range(screen_width):
				all_pixels.append(pixels[x,y])
		client.put_pixels(all_pixels, channel=0)
		#print i
		time.sleep(frame_delay)

