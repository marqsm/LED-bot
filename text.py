# coding=UTF-8
# Hacker School LED Display

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
frame_delay = 0.02
font = ImageFont.truetype("/Library/Fonts/Arial.ttf",14)
make_rainbows = False

# if argv 
def get_text():
	if len(sys.argv) > 1:
		return sys.argv[1]+"   "
	else:
		return "Hello, Hacker School!   "

#rainbow bg
def rainbow_bg(x,total):
	# hue, lightness, saturation to rgb 
	vals = colorsys.hls_to_rgb(round(float(x)/total,2),0.05,1)
	return (int(vals[0]*255),int(vals[1]*255),int(vals[2]*255))

def generate_img():
	all_pixels = []
	img_width,img_height = im.size
	for y in range(screen_height):
		for x in range(screen_width):
			all_pixels.append(pixels[x,y])
	return all_pixels
	
my_text = get_text() + "   " + get_text() 	
message_width, message_height = font.getsize(my_text)

im = Image.new("RGB",(screen_width,screen_height),"black")
draw = ImageDraw.Draw(im)
msg_width = int(message_width / 2)
total_width = message_width + screen_width

client = opc.Client(target_address)

print "Screen Width: %s Message Width: %s, Total Width: %s" % (screen_width,message_width,total_width) 

xOffset = 0
while True:
	# bg stuff
	if make_rainbows:
		rainbow_bg(xOffset,total_width)
	else:
		bg = (0,0,0)

	# Loop drawing one frame
	if xOffset > (msg_width + screen_width):
		xOffset -= msg_width
	else:
		xOffset += 1 

	print "Iteration: %s Drawing Offset: %s" % (xOffset,screen_width-xOffset)
	
	im.paste(bg,(0,0,screen_width,screen_height))
	
	draw.text((screen_width-xOffset,0), my_text, font=font)
	
	all_pixels = []
	pixels = im.load()

	client.put_pixels(generate_img(), channel=0)
	time.sleep(frame_delay)

