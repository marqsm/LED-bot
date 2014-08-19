# coding=UTF-8
# Hacker School LED Display

import time
import random
import opc
import colorsys
import sys
from marquee import Marquee_Text,Marquee_Data_Helpers
from PIL import Image,ImageFont,ImageDraw


target_address = '192.168.7.2:7890'
client = opc.Client(target_address)
marq = Marquee_Text();
data_helper = Marquee_Data_Helpers()

if client.can_connect():
	print 'Connected to OPC Server at %s' % (target_address)
else:
	print 'Could not connect to %s' % (target_address)

marq.make_message(["Never Graduate",data_helper.get_time(),"I'm a teapot","does this really work?","Maybe this message will display properly!"])

xOffset = 0
while 1:

	# Loop drawing one frame
	if marq.time_to_reloop(xOffset):
		xOffset -= marq.msg_width
	else:
		xOffset += 1 

	print "Iteration: %s" % (xOffset)
	marq.draw_text(xOffset)

	client.put_pixels(marq.slice_pixels(), channel=0)
	time.sleep(0.02)

