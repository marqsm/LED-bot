from slackclient import SlackClient
import os,sys,time,logging,re

class slackRequestHandler(object):
	def __init__(self,token=""):
		self.token = token
		self.client = None
		self.last_ping = 0
		self.id = None
		self.name = None
		self.selector = None
		self.callback = None

	def connect(self):
		self.slack_client = SlackClient(self.token)

		try:
			self.slack_client.rtm_connect()
			self.login_data = self.slack_client.server.login_data
			self.id = self.login_data["self"]["id"]
			self.name = self.login_data["self"]["name"]
			self.selector = re.compile("^<@"+self.id+">: (.*)")
		except Exception, e:
			print "failed to connect"

	def listen(self,callback):
		self.callback = callback
		self.start()

	def start(self):
		self.connect()
		while True:
			for reply in self.slack_client.rtm_read():
				if reply["type"] == "message":
					sender = self.slack_client.api_call("users.info",user=reply["user"])
					#print "%r said" % sender['user']["name"]
					tmp = re.search(self.selector,reply["text"]) 
					if tmp != None:
						print "direct message: %s" % tmp
						self.send_text(tmp.group(1))
			#	self.input(reply)
			self.ping()
			time.sleep(1)

	def ping(self):
		now = int(time.time())
		if now > self.last_ping + 10:
			self.slack_client.server.ping()
			self.last_ping = now
			#print "ping!"

	def input(self,data):
		if "type" in data:
			print dir(data)


	def send_text(self,data="blank message",color=(255,0,0),background=(0,0,0)):

		print ("trying to send",data)
		msg = {
			'text': data.split(),
			'type':'text',
			'color':color,
			'background':(0,0,0)
		}
		try:
			self.callback(msg, self)
		except:
			print "err with callback"
