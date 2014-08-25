from PIL import Image,ImageFont,ImageDraw
import opc
import time
im = Image.open('./test/doge.jpg')
#im = im.convert("RGB")

img_w, img_h = im.size
screen_w =64
screen_h = 32

img_ratio = img_w / img_h / 1.0
screen_ratio = screen_w / screen_h / 1.0

print "ratios img:%r scr:%r" % (img_ratio , screen_ratio)

def fit_to_screen():
	if screen_ratio > img_ratio:
		return (img_w * screen_h / img_h , screen_h)
	else:
		return (screen_w, img_h * screen_w / img_w)

print fit_to_screen()

#im = im.resize(ratio(), Image.NEAREST) 

im_w, im_h = im.size

print im_w,im_h

target_address = '10.0.5.184:7890'
client = opc.Client(target_address)
if client.can_connect():
	print 'Connected to OPC Server at %s' % (target_address)
else:
	print 'Could not connect to %s' % (target_address)

def slice_pixels(im):
		pixels = im2.load()
		print pixels
		all_pixels = []
		#img_width,img_height = self.im.size
		for y in range(screen_h):
			for x in range(screen_w):
				try:
					all_pixels.append(pixels[x,y])
				except IndexError:
					all_pixels.append((0,0,0))
		return all_pixels


xOffset = 0
img_dir = 1
#try:
#im.seek(1)
pixels = im.load()
print pixels
while 1:
	try:
			#im.seek(im.tell()+img_dir)
			im2 = im.convert("RGB")
			client.put_pixels(slice_pixels(im2), channel=0)
			#print "sending frame"
			time.sleep(0.2)
			# do something to im
	except EOFError:
	    im.seek(0)


