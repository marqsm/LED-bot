# coding=UTF-8
# Hacker School LED Display

import time
import random
import colorsys
import sys
from PIL import Image,ImageFont,ImageDraw

class Marquee_Text(object):
	"""Make text appear on the LED Matrix"""
	def __init__(self,height=32,width=64,font="/Library/Fonts/Verdana.ttf",font_color=(0,120,0),color_bg=False):

		# params
		self.screen_height = height
		self.screen_width = width
		self.color_bg = color_bg
		self.font_color = font_color
		self.text_to_send = " "
		self.color_cnt = 0

		# sizing set to 0
		self.total_width = 0
		self.msg_width = 0
		self.msg_height = 0
		self.single_msg_width = 0

		# new image and font
		self.font = ImageFont.truetype("./NotoSansCJK-Bold.otf",22)
		self.im = Image.new("RGB",(self.screen_width,self.screen_height),(120,0,0))
		self.draw = draw = ImageDraw.Draw(self.im)



	def rainbow_bg(c):
		# hue, lightness, saturation to rgb
		vals = colorsys.hls_to_rgb(round(c/360.0,2),0.05,1)
		return (int(vals[0]*255),int(vals[1]*255),int(vals[2]*255))

	def text_from_list(self,in_list):
		return "  ".join(in_list)

	def text_format(self,to_text):
		gap = "   "
		if len(to_text) > 1:
			return to_text + gap + to_text + gap
		else:
			return "Nice try, you sent an empty string.   Nice try, you sent an empty string.   "

	def time_to_reloop(self,offset):
		if offset > (self.msg_width + self.screen_width):
			return True
		else:
			return False

	def make_message(self,my_list):
		self.text_to_send = self.text_format(unicode(self.text_from_list(my_list),'UTF-8'))
		self.msg_width, self.msg_height = self.font.getsize(self.text_to_send)

		self.single_msg_width = int(self.msg_width / 2)
		self.total_width = self.msg_width + self.screen_width

	def draw_text(self,offset):
		self.im.paste((0,0,0),(0,0,self.screen_width,self.screen_height))
		self.draw.text((self.screen_width-offset,0), self.text_to_send, font=self.font,fill=self.font_color)

	def slice_pixels(self):
		pixels = self.im.load()
		all_pixels = []
		img_width,img_height = self.im.size
		for y in range(self.screen_height):
			for x in range(self.screen_width):
				all_pixels.append(pixels[x,y])
		return all_pixels

class Marquee_Data_Helpers(object):
	"""Make text appear on the LED Matrix"""
	def __init__(self):
		self.data = ""

	def get_weather(self,zip=10013):
		return "81 F in New York. It will rain tonight"

	def get_time(self):
		return time.strftime("%d %b %H:%M %p", time.localtime())

	def get_quote(self):
		return "Never trust a computer you can't throw out a window. - Steve Wozniak"

	def get_train_schedule(self):
		return "Train Schedule"

