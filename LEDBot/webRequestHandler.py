import datetime
import time
from threading import Thread
from os.path import dirname, exists, join
from bottle import route, request, run, template, Bottle, static_file

class WebRequestHandler:
	"""WebRequestHandler, a RESTful API"""
	def __init__(self,host='0.0.0.0',port=4000):
		self.here = dirname(__file__)
		self.www = Bottle()
		self.callback = None
		self.routes()

		server = Thread(target=self.www.run,kwargs=dict(host=host, port=port));
		server.setDaemon(True)
		server.start()

	def send_response(self, response, msg):
		""" Send the response to a user who sent a message to us. """
		return response["content"]


	def listen(self,callback):
		self.callback = callback

	def send_text(self,data="blank message",color=(0,255,0)):

		print ("trying to send",data)
		msg = {
			'text': data.split(),
			'type':'text',
			'color':color,
			'background':(0,0,0)
		}
		self.callback(msg, self)

	def send_image(self,data):
		msg = {
			'url': data,
			'type':'image'
		}
		self.callback(msg, self)


	def send_system_message(self,content):
		msg = {
			'type':'system',
			'text': content
		}
		self.callback(msg, self)


	def routes(self):

		@self.www.route('/')
		def index():
		    return static_file('index.html', root=join(self.here,"www/"))

		@self.www.post('/show-text/')
		def show_text():
			color = (0,255,0)
			if 'message' in request.forms: 
				if 'color' in request.forms:
					color = tuple([int(i) for i in request.forms.color.split(",")])
				self.send_text(request.forms.message,color)
				print 'Your message %s! In color %s</b>' % (request.forms.message, color)

		@self.www.post('/show-image/')
		def show_image():
			self.send_image(request.forms.url)
			print 'image URL: %s' % (request.forms.url)

		@self.www.get('/static/<filename:path>')
		def send_static(filename):
		    return static_file(filename, root=join(self.here,"www/"))


