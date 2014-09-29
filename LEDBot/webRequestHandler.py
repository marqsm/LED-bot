import datetime
from bottle import route, request, run, template, Bottle
from threading import Thread
import time
class WebRequestHandler(object):
	"""docstring for WebRequestHandler"""
	def __init__(self):
		self.www = Bottle()
		self.callback = None

		@self.www.post('/show-text/')
		def show_text():
			self.send_text(request.forms.message,int(request.forms.r),int(request.forms.g),int(request.forms.b))
			print 'Your message %s! In color %s, %s, %s</b>' % (request.forms.message, request.forms.r,request.forms.g,request.forms.b)

		@self.www.post('/show-image/')
		def show_image():
			self.send_image(request.forms.url)
			print 'image URL: %s' % (request.forms.url)

		@self.www.route('/hello/<name>')
		def index(name):
			return template('<b>Hello {{name}}</b>!', name=name)

		server = Thread(target=self.www.run,kwargs=dict(host='localhost', port=4000));
		server.setDaemon(True)
		server.start()

	def send_response(self, response, msg):
		""" Send the response to a user who sent a message to us. """

	def listen(self,callback):
		self.callback = callback
		#self.send_new_message()

	def send_text(self,data,r=0,g=0,b=120):

		print ("trying to send",data)
		msg = {
			'text': data.split(),
			'type':'text',
			'color':(r,g,b),
			'background':(0,0,0)
		}
		self.callback(msg, self)

	def send_image(self,data):
		msg = {
			'url': data,
			'type':'image'
		}
		self.callback(msg, self)